using Google.Protobuf.WellKnownTypes;
using Grpc.Core;
using Grpc.Net.Client;

namespace Noffz.Dut.Grpc.Client;

/// <summary>
/// Thin async wrapper over the generated DutControl client.
///
///   using var dut = new DutClient("http://instrument-pc:50051");
///   await dut.OpenSessionAsync("COM5");
///   await dut.StartWlanTxAsync(6, WlanDataRate.G6M);
///   ...
///   await dut.StopAsync();
///
/// Server errors surface as RpcException (StatusCode.FailedPrecondition when
/// no session is open or the DUT is in the wrong mode, DeadlineExceeded when
/// the firmware doesn't answer, Unavailable for serial port errors).
/// </summary>
public sealed class DutClient : IDisposable
{
    private readonly GrpcChannel _channel;
    private readonly DutControl.DutControlClient _client;

    /// <param name="address">"http://host:50051" or "host:50051".</param>
    public DutClient(string address)
    {
        if (!address.StartsWith("http://", StringComparison.OrdinalIgnoreCase) &&
            !address.StartsWith("https://", StringComparison.OrdinalIgnoreCase))
            address = "http://" + address;

        _channel = GrpcChannel.ForAddress(address);
        _client = new DutControl.DutControlClient(_channel);
    }

    /// <summary>Per-call deadline. Should exceed the service's ReadTimeoutMs.</summary>
    public TimeSpan CallTimeout { get; set; } = TimeSpan.FromSeconds(15);

    /// <summary>The generated client, for anything the wrapper doesn't cover.</summary>
    public DutControl.DutControlClient Raw => _client;

    #region session
    public async Task<SessionStatus> OpenSessionAsync(string port = "", int readTimeoutMs = 0,
                                                      CancellationToken ct = default) =>
        await _client.OpenSessionAsync(
            new OpenSessionRequest { Port = port ?? "", ReadTimeoutMs = readTimeoutMs }, Options(ct));

    public async Task<SessionStatus> CloseSessionAsync(CancellationToken ct = default) =>
        await _client.CloseSessionAsync(new Empty(), Options(ct));

    public async Task<SessionStatus> GetStatusAsync(CancellationToken ct = default) =>
        await _client.GetStatusAsync(new Empty(), Options(ct));

    public async Task<CommandReply> StopAsync(CancellationToken ct = default) =>
        await _client.StopAsync(new Empty(), Options(ct));
    #endregion

    #region Wi-Fi
    /// <param name="attenuationDb">TX power reduction in dB (0.25 dB resolution).</param>
    public async Task<CommandReply> StartWlanTxAsync(int channel, WlanDataRate rate,
                                                     double attenuationDb = 0,
                                                     WlanBandwidth bandwidth = WlanBandwidth.Ht20,
                                                     CancellationToken ct = default) =>
        await _client.StartWlanTxAsync(new WlanTxRequest
        {
            Channel = channel,
            Rate = rate,
            AttenuationQuarterDb = (int)Math.Round(attenuationDb * 4),
            Bandwidth = bandwidth,
        }, Options(ct));

    public async Task<CommandReply> StartWlanRxAsync(int channel, WlanDataRate rate,
                                                     WlanBandwidth bandwidth = WlanBandwidth.Ht20,
                                                     CancellationToken ct = default) =>
        await _client.StartWlanRxAsync(new WlanRxRequest
        {
            Channel = channel,
            Rate = rate,
            Bandwidth = bandwidth,
        }, Options(ct));

    public async Task<WlanRxResult> FetchWlanRxAsync(CancellationToken ct = default) =>
        await _client.FetchWlanRxAsync(new Empty(), Options(ct));
    #endregion

    #region BLE
    public async Task<CommandReply> StartBleTxAsync(int channelIndex, int powerLevel = 15,
                                                    int payloadLength = 250,
                                                    BlePayloadPattern pattern = BlePayloadPattern.Prbs9,
                                                    BleRate rate = BleRate.Le1M,
                                                    uint syncWord = 0,
                                                    int transmissionMode = 0,
                                                    CancellationToken ct = default) =>
        await _client.StartBleTxAsync(new BleTxRequest
        {
            ChannelIndex = channelIndex,
            PowerLevel = powerLevel,
            PayloadLength = payloadLength,
            PayloadPattern = pattern,
            Rate = rate,
            SyncWord = syncWord,
            TransmissionMode = transmissionMode,
        }, Options(ct));

    public async Task<CommandReply> StartBleRxAsync(int channelIndex, BleRate rate = BleRate.Le1M,
                                                    uint syncWord = 0,
                                                    CancellationToken ct = default) =>
        await _client.StartBleRxAsync(new BleRxRequest
        {
            ChannelIndex = channelIndex,
            Rate = rate,
            SyncWord = syncWord,
        }, Options(ct));

    public async Task<BleRxResult> FetchBleRxAsync(CancellationToken ct = default) =>
        await _client.FetchBleRxAsync(new Empty(), Options(ct));
    #endregion

    private CallOptions Options(CancellationToken ct) =>
        new(deadline: DateTime.UtcNow.Add(CallTimeout), cancellationToken: ct);

    public void Dispose() => _channel.Dispose();
}

/// <summary>PER helpers for the RX results.</summary>
public static class RxResultExtensions
{
    public static double Per(this WlanRxResult r, int sent) =>
        sent > 0 ? 1.0 - (double)r.DesiredPackets / sent : double.NaN;

    public static double Per(this BleRxResult r, int sent) =>
        sent > 0 ? 1.0 - (double)r.DesiredPackets / sent : double.NaN;
}
