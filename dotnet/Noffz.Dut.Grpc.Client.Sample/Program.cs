// Smoke test for the DUT service: exercises every call once.
//   dotnet run --project Noffz.Dut.Grpc.Client.Sample -- http://localhost:50051 COM5
using Grpc.Core;
using Noffz.Dut.Grpc;
using Noffz.Dut.Grpc.Client;

string address = args.Length > 0 ? args[0] : "http://localhost:50051";
string port = args.Length > 1 ? args[1] : "";

using var dut = new DutClient(address);

try
{
    Console.WriteLine($"Open:   {await dut.OpenSessionAsync(port)}");

    Console.WriteLine($"WLAN TX ch6 6M: {await dut.StartWlanTxAsync(6, WlanDataRate.G6M)}");
    await Task.Delay(2000);
    Console.WriteLine($"Stop:   {await dut.StopAsync()}");

    Console.WriteLine($"BLE TX idx19:   {await dut.StartBleTxAsync(19, powerLevel: 15)}");
    await Task.Delay(2000);
    Console.WriteLine($"Stop:   {await dut.StopAsync()}");

    await dut.StartWlanRxAsync(6, WlanDataRate.G6M);
    await Task.Delay(2000);
    WlanRxResult wlan = await dut.FetchWlanRxAsync();
    Console.WriteLine($"WLAN RX: correct={wlan.CorrectPackets} desired={wlan.DesiredPackets} rssi={wlan.RssiDbm:F1}");

    await dut.StartBleRxAsync(19);
    await Task.Delay(2000);
    BleRxResult ble = await dut.FetchBleRxAsync();
    Console.WriteLine($"BLE RX:  total={ble.TotalPackets} desired={ble.DesiredPackets} rssi={ble.RssiDbm:F1}");

    Console.WriteLine($"Status: {await dut.GetStatusAsync()}");
}
catch (RpcException ex)
{
    Console.Error.WriteLine($"gRPC error {ex.StatusCode}: {ex.Status.Detail}");
    return 1;
}
return 0;
