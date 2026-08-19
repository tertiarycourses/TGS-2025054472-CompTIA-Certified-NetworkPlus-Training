# Lab 11 checklist — Wireless Concepts and Channel Survey

This lab runs on **your own laptop**, not the Killercoda playground — the
playground has no radio. Tick each box as you complete it.

- [ ] Installed a survey tool for your OS (`iw` + `wavemon` on Linux, WiFi Analyzer or Acrylic Wi-Fi Home on Windows, Wireless Diagnostics on macOS)
- [ ] Ran `iw list` (or the equivalent) and identified which bands your adapter supports: 2.4 / 5 / 6 GHz
- [ ] Identified the HT / VHT / HE capability lines and can say which Wi-Fi generation each maps to
- [ ] Scanned nearby APs and recorded SSID, BSSID, channel, band, signal (dBm) and security for each
- [ ] Added at least five of your own rows to `data/site-survey.csv` alongside the example rows
- [ ] Can explain why 1, 6 and 11 are the only non-overlapping 2.4 GHz channels
- [ ] Found at least one pair of APs on overlapping 2.4 GHz channels in your survey and can say why that hurts throughput
- [ ] Can explain what DFS is and why a radar detection causes a brief outage
- [ ] Can rank the security modes in your survey from weakest to strongest (WEP → WPA2-PSK → WPA2-Enterprise → WPA3-SAE → WPA3-Enterprise 192-bit)
- [ ] Can explain why Wi-Fi 6E (6 GHz) requires WPA3
- [ ] Answered all three Step 5 quiz questions out loud to a partner
- [ ] **Test it:** your completed `data/site-survey.csv` has one row per AP your scan found, with the channel and security columns filled in, and you can point to the strongest and the weakest-secured AP in the list
