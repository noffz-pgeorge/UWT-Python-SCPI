using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO.Ports;
using System.Text.RegularExpressions;

namespace Noffz.Espressif.ESP32C3.DutControls
{
    /// <summary>
    /// Controls an ESP32-C3 running Espressif's RF non-signaling test firmware.
    ///
    /// Changes from the original version (public API is source-compatible;
    /// command strings are unchanged):
    ///  - Read/write timeouts (ReadTimeoutMs). The original SerialPort used an
    ///    infinite ReadTimeout, so a missing response blocked forever.
    ///  - Commands that only print an acknowledgement tolerate no reply
    ///    instead of blocking.
    ///  - The input buffer is cleared before each command, and RX fetches read
    ///    lines until the result line appears, so a stray line can't shift
    ///    every following response by one.
    ///  - BtRxFetch parses the packet counts as hexadecimal (the firmware
    ///    prints e.g. "3e8" = 1000; Convert.ToInt32("3e8") threw).
    ///  - New BtRxFetchResult / WlanRxFetchResult return total, desired and
    ///    RSSI. Use Desired for PER: it counts packets at the configured rate.
    ///  - Console output goes through the Log delegate (Console by default).
    ///  - TX/RX start methods and AbortTx return the firmware's reply line.
    /// </summary>
    public class ESP32C3Control
    {
        private SerialPort _dut;

        private static readonly Regex WlanRxRegex = new Regex(
            @"Correct:\s*(\d+)\s+Desired:\s*(\d+)\s+RSSI:\s*(-?\d+)",
            RegexOptions.Compiled);

        /// <summary>Timeout for responses the firmware must send (RX results).</summary>
        public int ReadTimeoutMs { get; set; } = 3000;

        /// <summary>How long to wait for an optional acknowledgement line.</summary>
        public int AckTimeoutMs { get; set; } = 500;

        /// <summary>Receives every line read from the DUT. Set to null to silence.</summary>
        public Action<string> Log { get; set; } = Console.WriteLine;

        public bool IsOpen => _dut != null && _dut.IsOpen;

        public string PortName => _dut?.PortName;

        public void OpenSession(string port)
        {
            _dut = new SerialPort(port, 115200, Parity.None, 8, StopBits.One)
            {
                ReadTimeout = ReadTimeoutMs,
                WriteTimeout = ReadTimeoutMs,
                // Keep DTR/RTS deasserted: on the dev kit's USB-UART bridge they
                // drive EN/BOOT and would reset the chip.
                DtrEnable = false,
                RtsEnable = false,
            };
            _dut.Open();
        }

        public string BtTxGenerate(
            int powerLevel,
            int channelNumber,
            int payloadLength,
            PayloadBitPattern payloadBitPattern,
            string syncw,
            TransmissionRate transmissionRate,
            int transmissionMode)
        {
            Send($"fcc_le_tx_syncw {powerLevel} {channelNumber} {payloadLength} {(int)payloadBitPattern} {syncw} {(int)transmissionRate} {transmissionMode}");
            return ReadAck();
        }

        public string AbortTx()
        {
            Send("cmdstop");
            return ReadAck();
        }

        public string BtRxListen(
            int channelNumber,
            string syncw,
            TransmissionRate transmissionRate)
        {
            Send($"rw_le_rx_per {channelNumber} {syncw} {(int)transmissionRate}");
            return ReadAck();
        }

        /// <summary>Stops BLE RX and returns the total packets received (Res[0]).</summary>
        public int BtRxFetch()
        {
            return BtRxFetchResult().Total;
        }

        /// <summary>Stops BLE RX and returns the parsed result line.</summary>
        public BtRxReading BtRxFetchResult()
        {
            Send("cmdstop");
            // e.g. "3e8 3e8 0 0 0 0 0 0 0 0 p -53276 -24131 0 29422"
            string line = ReadUntil(IsBtRxLine, "BLE RX result");
            string[] t = Tokens(line);

            var reading = new BtRxReading(
                Convert.ToInt32(t[0], 16),
                Convert.ToInt32(t[1], 16),
                long.Parse(t[11], CultureInfo.InvariantCulture),
                line);

            Log?.Invoke($"Pkt: {reading.Total}, with corresponding rate: {reading.Desired}, RSSI: {reading.RssiDbm:F1} dBm");
            return reading;
        }

        public string WlanTxGenerate(
            int channel,
            WlanDataRate dataRate,
            sbyte attenuation,
            WlanBandwidth htMode)
        {
            Send($"cbw40m_en {(int)htMode}");
            ReadAck();

            Send($"wifitxout {channel} 0x{(int)dataRate:x} {attenuation}");
            return ReadAck();
        }

        public string WlanRxListen(int channel, WlanDataRate dataRate, WlanBandwidth htMode)
        {
            Send($"cbw40m_en {(int)htMode}");
            ReadAck();

            Send($"esp_rx {channel} 0x{(int)dataRate:x}");
            return ReadAck();
        }

        /// <summary>Stops Wi-Fi RX and returns the "Correct" packet count.</summary>
        public int WlanRxFetch()
        {
            return WlanRxFetchResult().Correct;
        }

        /// <summary>Stops Wi-Fi RX and returns the parsed result line.</summary>
        public WlanRxReading WlanRxFetchResult()
        {
            Send("cmdstop");
            string line = ReadUntil(l => WlanRxRegex.IsMatch(l), "Wi-Fi RX result");
            GroupCollection g = WlanRxRegex.Match(line).Groups;

            return new WlanRxReading(
                int.Parse(g[1].Value, CultureInfo.InvariantCulture),
                int.Parse(g[2].Value, CultureInfo.InvariantCulture),
                int.Parse(g[3].Value, CultureInfo.InvariantCulture) / 10.0,
                line);
        }

        public void CloseSession()
        {
            if (_dut == null)
                return;
            if (_dut.IsOpen)
                _dut.Close();
            _dut.Dispose();
            _dut = null;
        }

        #region serial helpers
        private void Send(string cmd)
        {
            if (!IsOpen)
                throw new InvalidOperationException("DUT session is not open. Call OpenSession first.");
            _dut.DiscardInBuffer();
            _dut.WriteLine(cmd + "\r");
        }

        /// <summary>Reads one line if the firmware sends one; null on timeout.</summary>
        private string ReadAck()
        {
            string line = TryReadLine(AckTimeoutMs);
            if (!string.IsNullOrEmpty(line))
                Log?.Invoke(line);
            return line;
        }

        /// <summary>Reads lines until one matches; throws TimeoutException otherwise.</summary>
        private string ReadUntil(Func<string, bool> isMatch, string what)
        {
            var seen = new List<string>();
            DateTime deadline = DateTime.UtcNow.AddMilliseconds(ReadTimeoutMs);

            while (DateTime.UtcNow < deadline)
            {
                int remaining = (int)Math.Max(1, (deadline - DateTime.UtcNow).TotalMilliseconds);
                string line = TryReadLine(remaining);
                if (line == null)
                    break;
                if (line.Length == 0)
                    continue;

                Log?.Invoke(line);
                if (isMatch(line))
                    return line;
                seen.Add(line);
            }

            throw new TimeoutException(
                $"No {what} from DUT within {ReadTimeoutMs} ms. Received: [{string.Join(" | ", seen)}]");
        }

        private string TryReadLine(int timeoutMs)
        {
            int previous = _dut.ReadTimeout;
            _dut.ReadTimeout = timeoutMs;
            try
            {
                return _dut.ReadLine().Trim();
            }
            catch (TimeoutException)
            {
                return null;
            }
            finally
            {
                _dut.ReadTimeout = previous;
            }
        }

        private static string[] Tokens(string line) =>
            line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);

        private static bool IsBtRxLine(string line)
        {
            string[] t = Tokens(line);
            return t.Length >= 12
                && t[10] == "p"
                && IsHex(t[0])
                && IsHex(t[1])
                && long.TryParse(t[11], NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out _);
        }

        private static bool IsHex(string s) =>
            int.TryParse(s, NumberStyles.AllowHexSpecifier, CultureInfo.InvariantCulture, out _);
        #endregion

        #region enums
        public enum PayloadBitPattern
        {
            Pattern_1010 = 0,
            Pattern_00001111 = 1,
            Pattern_PRBS9 = 2,
        }

        public enum TransmissionRate
        {
            Rate_1M = 0,
            Rate_2M = 1,
            Rate_125k = 2,
            Rate_500k = 3
        }

        // Values are the firmware's rate codes. Any code can be cast in, e.g.
        // (WlanDataRate)0x10 for MCS0.
        public enum WlanDataRate
        {
            Rate_11b_1M = 0,
            Rate_11b_2M = 1,

            Rate_11g_6M = 11,
            Rate_11g_9M = 15,
            Rate_11g_54M = 13,   // NOTE: esp_phy_cert_test.h lists 0xC (12) as 54M and 0xD (13) as 36M
            Rate_11n_MCS7 = 23,
        }

        public enum WlanBandwidth
        {
            HT20 = 0,
            HT40 = 1
        }
        #endregion
    }

    /// <summary>One BLE RX result: Res[0], Res[1] and Res[11] from the firmware.</summary>
    public sealed class BtRxReading
    {
        public BtRxReading(int total, int desired, long rssiSum, string raw)
        {
            Total = total;
            Desired = desired;
            RssiSum = rssiSum;
            Raw = raw;
        }

        public int Total { get; }
        public int Desired { get; }
        public long RssiSum { get; }
        public string Raw { get; }
        public double RssiDbm => Desired > 0 ? (double)RssiSum / Desired : double.NaN;
    }

    /// <summary>One Wi-Fi RX result line.</summary>
    public sealed class WlanRxReading
    {
        public WlanRxReading(int correct, int desired, double rssiDbm, string raw)
        {
            Correct = correct;
            Desired = desired;
            RssiDbm = rssiDbm;
            Raw = raw;
        }

        public int Correct { get; }
        public int Desired { get; }
        public double RssiDbm { get; }
        public string Raw { get; }
    }
}
