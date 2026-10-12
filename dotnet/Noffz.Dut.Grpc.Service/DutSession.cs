using Grpc.Core;
using Microsoft.Extensions.Options;
using Noffz.Espressif.ESP32C3.DutControls;

namespace Noffz.Dut.Grpc.Service;

/// <summary>
/// Owns the one ESP32C3Control instance and its serial port. Every call goes
/// through a single gate, so concurrent gRPC calls run one at a time and the
/// firmware never sees interleaved commands. Also tracks the DUT's mode so a
/// Fetch can't be called against the wrong RX mode.
/// </summary>
public sealed class DutSession : IDisposable
{
    private readonly SemaphoreSlim _gate = new(1, 1);
    private readonly DutOptions _options;
    private readonly ILogger<DutSession> _log;
    private ESP32C3Control? _ctl;

    public DutSession(IOptions<DutOptions> options, ILogger<DutSession> log)
    {
        _options = options.Value;
        _log = log;
    }

    public DutState State { get; private set; } = DutState.Closed;

    #region session
    public Task<SessionStatus> OpenAsync(string port, int readTimeoutMs, CancellationToken ct) =>
        RunAsync(() =>
        {
            port = string.IsNullOrWhiteSpace(port) ? _options.DefaultPort : port.Trim();
            if (string.IsNullOrWhiteSpace(port))
                throw new RpcException(new Status(StatusCode.InvalidArgument,
                    "No port given and no Dut:DefaultPort configured."));

            if (_ctl is { IsOpen: true } &&
                string.Equals(_ctl.PortName, port, StringComparison.OrdinalIgnoreCase))
                return BuildStatus();

            CloseCore();

            var ctl = new ESP32C3Control
            {
                ReadTimeoutMs = readTimeoutMs > 0 ? readTimeoutMs : _options.ReadTimeoutMs,
                Log = line => _log.LogDebug("DUT << {Line}", line),
            };
            ctl.OpenSession(port);
            _ctl = ctl;
            State = DutState.Idle;
            _log.LogInformation("Opened DUT session on {Port}", port);
            return BuildStatus();
        }, ct, requireOpen: false);

    public Task<SessionStatus> CloseAsync(CancellationToken ct) =>
        RunAsync(() =>
        {
            CloseCore();
            return BuildStatus();
        }, ct, requireOpen: false);

    public Task<SessionStatus> GetStatusAsync(CancellationToken ct) =>
        RunAsync(BuildStatus, ct, requireOpen: false);

    /// <summary>Opens Dut:DefaultPort at startup when Dut:AutoOpen is true.</summary>
    public void TryAutoOpen()
    {
        if (!_options.AutoOpen || string.IsNullOrWhiteSpace(_options.DefaultPort))
            return;
        try
        {
            OpenAsync("", 0, CancellationToken.None).GetAwaiter().GetResult();
        }
        catch (Exception ex)
        {
            _log.LogWarning(ex, "Auto-open of {Port} failed; clients can call OpenSession later",
                _options.DefaultPort);
        }
    }
    #endregion

    #region operations
    /// <summary>Stops whatever is running, then starts a new TX/RX mode.</summary>
    public Task<CommandReply> StartAsync(DutState next, Func<ESP32C3Control, string?> start,
                                         CancellationToken ct) =>
        RunAsync(() =>
        {
            if (State != DutState.Idle)
            {
                _ctl!.AbortTx();
                State = DutState.Idle;
            }

            string? response = start(_ctl!);
            State = next;
            _log.LogInformation("DUT -> {State}", next);
            return new CommandReply { Response = response ?? "", State = State };
        }, ct);

    public Task<CommandReply> StopAsync(CancellationToken ct) =>
        RunAsync(() =>
        {
            string? response = _ctl!.AbortTx();
            State = DutState.Idle;
            return new CommandReply { Response = response ?? "", State = State };
        }, ct);

    /// <summary>Stops RX and reads the result. The DUT is idle afterwards either way.</summary>
    public Task<T> FetchAsync<T>(DutState expected, Func<ESP32C3Control, T> fetch, CancellationToken ct) =>
        RunAsync(() =>
        {
            if (State != expected)
                throw new RpcException(new Status(StatusCode.FailedPrecondition,
                    $"DUT is in state {State}; start {expected} before fetching."));
            try
            {
                return fetch(_ctl!);
            }
            finally
            {
                State = DutState.Idle;
            }
        }, ct);
    #endregion

    #region plumbing
    private async Task<T> RunAsync<T>(Func<T> op, CancellationToken ct, bool requireOpen = true)
    {
        await _gate.WaitAsync(ct);
        try
        {
            if (requireOpen && _ctl is not { IsOpen: true })
                throw new RpcException(new Status(StatusCode.FailedPrecondition,
                    "No DUT session is open. Call OpenSession first."));

            // Serial I/O is blocking; keep it off the request thread. Not
            // cancellable mid-command, so the port never sees half a command.
            return await Task.Run(op, CancellationToken.None);
        }
        catch (RpcException)
        {
            throw;
        }
        catch (TimeoutException ex)
        {
            throw new RpcException(new Status(StatusCode.DeadlineExceeded, ex.Message));
        }
        catch (ArgumentException ex)
        {
            throw new RpcException(new Status(StatusCode.InvalidArgument, ex.Message));
        }
        catch (FormatException ex)
        {
            throw new RpcException(new Status(StatusCode.Internal, "Unexpected DUT response: " + ex.Message));
        }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException or InvalidOperationException)
        {
            _log.LogError(ex, "Serial port error");
            throw new RpcException(new Status(StatusCode.Unavailable, "Serial port error: " + ex.Message));
        }
        catch (Exception ex)
        {
            _log.LogError(ex, "Unhandled DUT error");
            throw new RpcException(new Status(StatusCode.Internal, ex.Message));
        }
        finally
        {
            _gate.Release();
        }
    }

    private SessionStatus BuildStatus() => new()
    {
        IsOpen = _ctl is { IsOpen: true },
        Port = _ctl?.PortName ?? "",
        State = State,
    };

    private void CloseCore()
    {
        if (_ctl is null)
            return;
        try
        {
            if (_ctl.IsOpen && State != DutState.Idle)
                _ctl.AbortTx();
        }
        catch (Exception ex)
        {
            _log.LogWarning(ex, "cmdstop before close failed");
        }
        try
        {
            _ctl.CloseSession();
        }
        catch (Exception ex)
        {
            _log.LogWarning(ex, "Closing serial port failed");
        }
        _log.LogInformation("Closed DUT session");
        _ctl = null;
        State = DutState.Closed;
    }

    public void Dispose()
    {
        CloseCore();
        _gate.Dispose();
    }
    #endregion
}
