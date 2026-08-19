# Lab 18 checklist — Time Synchronisation with Chrony

Tick each item as you complete it.

- [ ] Installed chrony with `apt install -y chrony` and started it with `systemctl enable --now chrony`
- [ ] Listed time sources with `chronyc sources -v`
- [ ] Identified the currently selected source by its `^*` symbol
- [ ] Read the stratum column and explained what Stratum 1 vs Stratum 3 means
- [ ] Ran `chronyc tracking` and read **Stratum**, **System time**, **Last offset** and **RMS offset**
- [ ] Read `chrony.conf.lab` and understood what `iburst` does before appending it
- [ ] Appended `server time.cloudflare.com iburst` to `/etc/chrony/chrony.conf`
- [ ] Restarted chrony and confirmed the new server appears in `chronyc sources -v`
- [ ] Forced an immediate correction with `chronyc -a makestep`
- [ ] Named the transport protocol and port NTP uses (UDP/123)
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `chronyd` is running, `chronyc sources` shows a `^*` selected source, `chronyc tracking` reports a usable stratum, and the Step 4 server is in `/etc/chrony/chrony.conf`
