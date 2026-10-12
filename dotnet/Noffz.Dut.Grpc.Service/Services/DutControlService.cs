using Google.Protobuf.WellKnownTypes;
using Grpc.Core;
using Noffz.Espressif.ESP32C3.DutControls;
using Ctl = Noffz.Espressif.ESP32C3.DutControls.ESP32C3Control;

namespace Noffz.Dut.Grpc.Service.Services;

/// <summary>gRPC endpoint. Validates requests and maps them onto ESP32C3Control.</summary>
public sealed class DutControlService : DutControl.DutControlBase
{
    private const uint DefaultSyncWord = 0x71764129;
    private const int DefaultBlePayloadLength = 250;

    private readonly DutSession _session;

    public DutControlService(DutSession session) => _session = session;

    #region session
    public override Task<SessionStatus> OpenSession(OpenSessionRequest request, ServerCallContext context) =>
        _session.OpenAsync(request.Port, request.ReadTimeoutMs, context.CancellationToken);

    public override Task<SessionStatus> CloseSession(Empty request, ServerCallContext context) =>
        _session.CloseAsync(context.CancellationToken);

    public override Task<SessionStatus> GetStatus(Empty request, ServerCallContext context) =>
        _session.GetStatusAsync(context.CancellationToken);

    public override Task<CommandReply> Stop(Empty request, ServerCallContext context) =>
        _session.StopAsync(context.CancellationToken);
    #endregion

    #region BLE
    public override Task<CommandReply> StartBleTx(BleTxRequest r, ServerCallContext context)
    {
        Require(r.PowerLevel is >= 0 and <= 15, "power_level must be 0..15");
        RequireBleChannel(r.ChannelIndex);
        Require(r.PayloadLength is >= 0 and <= 255, "payload_length must be 0..255");
        int length = r.PayloadLength == 0 ? DefaultBlePayloadLength : r.PayloadLength;
        string syncw = SyncWord(r.SyncWord);

        return _session.StartAsync(DutState.BleTx, c => c.BtTxGenerate(
            r.PowerLevel,
            r.ChannelIndex,
            length,
            (Ctl.PayloadBitPattern)(int)r.PayloadPattern,
            syncw,
            (Ctl.TransmissionRate)(int)r.Rate,
            r.TransmissionMode), context.CancellationToken);
    }

    public override Task<CommandReply> StartBleRx(BleRxRequest r, ServerCallContext context)
    {
        RequireBleChannel(r.ChannelIndex);
        string syncw = SyncWord(r.SyncWord);

        return _session.StartAsync(DutState.BleRx, c => c.BtRxListen(
            r.ChannelIndex, syncw, (Ctl.TransmissionRate)(int)r.Rate), context.CancellationToken);
    }

    public override Task<BleRxResult> FetchBleRx(Empty request, ServerCallContext context) =>
        _session.FetchAsync(DutState.BleRx, c =>
        {
            BtRxReading x = c.BtRxFetchResult();
            return new BleRxResult
            {
                TotalPackets = x.Total,
                DesiredPackets = x.Desired,
                RssiDbm = x.RssiDbm,
                Raw = x.Raw,
            };
        }, context.CancellationToken);
    #endregion

    #region Wi-Fi
    public override Task<CommandReply> StartWlanTx(WlanTxRequest r, ServerCallContext context)
    {
        RequireWlanChannel(r.Channel);
        Require(r.AttenuationQuarterDb is >= -128 and <= 127,
            "attenuation_quarter_db must fit in a signed byte (-128..127)");

        return _session.StartAsync(DutState.WlanTx, c => c.WlanTxGenerate(
            r.Channel,
            (Ctl.WlanDataRate)(int)r.Rate,
            (sbyte)r.AttenuationQuarterDb,
            (Ctl.WlanBandwidth)(int)r.Bandwidth), context.CancellationToken);
    }

    public override Task<CommandReply> StartWlanRx(WlanRxRequest r, ServerCallContext context)
    {
        RequireWlanChannel(r.Channel);

        return _session.StartAsync(DutState.WlanRx, c => c.WlanRxListen(
            r.Channel,
            (Ctl.WlanDataRate)(int)r.Rate,
            (Ctl.WlanBandwidth)(int)r.Bandwidth), context.CancellationToken);
    }

    public override Task<WlanRxResult> FetchWlanRx(Empty request, ServerCallContext context) =>
        _session.FetchAsync(DutState.WlanRx, c =>
        {
            WlanRxReading x = c.WlanRxFetchResult();
            return new WlanRxResult
            {
                CorrectPackets = x.Correct,
                DesiredPackets = x.Desired,
                RssiDbm = x.RssiDbm,
                Raw = x.Raw,
            };
        }, context.CancellationToken);
    #endregion

    #region validation
    private static string SyncWord(uint value) =>
        $"0x{(value == 0 ? DefaultSyncWord : value):x8}";

    private static void RequireBleChannel(int index) =>
        Require(index is >= 0 and <= 39, "channel_index must be 0..39");

    private static void RequireWlanChannel(int channel) =>
        Require(channel is >= 1 and <= 14, "channel must be 1..14");

    private static void Require(bool ok, string message)
    {
        if (!ok)
            throw new RpcException(new Status(StatusCode.InvalidArgument, message));
    }
    #endregion
}
