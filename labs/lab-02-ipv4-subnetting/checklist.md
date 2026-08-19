# Lab 2 checklist — IPv4 Subnetting and CIDR

Tick each item as you complete it.

- [ ] Opened the TIS IP Calculator at https://alfredang.github.io/ipcalculator/ in a browser tab
- [ ] Entered `192.168.10.0/24` and read off network, broadcast, host range, mask and host counts
- [ ] Explained why a `/24` gives 256 total and 254 usable addresses
- [ ] Calculated all four `/26` subnets: `.0`, `.64`, `.128`, `.192`
- [ ] Completed the Step 3 table with network, first host, last host and broadcast for each subnet
- [ ] Confirmed each `/26` has 64 total addresses and 62 usable hosts
- [ ] Opened `data/subnet-plan.csv` and filled in the CIDR, network, first host, last host and broadcast columns for all 12 department rows
- [ ] Allocated each site largest-requirement-first so no address space overlaps
- [ ] Checked my work against `answers.md`
- [ ] Assigned the address with `ip addr add 192.168.10.65/26 dev eth0 label eth0:1`
- [ ] Removed the address with `ip addr del 192.168.10.65/26 dev eth0`
- [ ] **Test it:** `ip -4 addr show eth0` shows `inet 192.168.10.65/26 ... eth0:1` before cleanup, and that line is gone after cleanup
