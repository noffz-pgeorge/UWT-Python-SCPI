namespace Noffz.Dut.Grpc.Service;

/// <summary>"Dut" section of appsettings.json.</summary>
public sealed class DutOptions
{
    public const string Section = "Dut";

    /// <summary>Serial port used when OpenSession is called with an empty port.</summary>
    public string DefaultPort { get; set; } = "";

    /// <summary>Open DefaultPort when the service starts.</summary>
    public bool AutoOpen { get; set; }

    /// <summary>How long to wait for RX results from the firmware.</summary>
    public int ReadTimeoutMs { get; set; } = 3000;
}
