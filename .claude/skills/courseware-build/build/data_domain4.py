"""Domain 4 — Network Security (14% of the N10-009 exam).

DOMAIN4  = the 7 hands-on labs (global nums 21-27).
CONTENT4 = the teaching slide specs, with one lab marker per lab.
"""

DOMAIN4 = [
    dict(
        num=21,
        topic=4,
        title="Host Firewall with UFW",
        objective="Configure a default-deny host firewall with UFW: global allows, source-restricted rules, rule management.",
        desc="Set a deny-by-default inbound policy with UFW, permit SSH globally and MySQL only from 10.0.0.0/8, then list, delete and disable rules to manage the firewall lifecycle.",
        build="A host firewall that denies all inbound traffic except SSH and source-restricted MySQL.",
        services="ufw, iptables",
        steps=[
            ("Install UFW", "apt update && apt install -y ufw"),
            ("Set deny-by-default inbound and allow outbound",
             "ufw default deny incoming && ufw default allow outgoing"),
            ("Allow SSH first - skipping this in a real session locks you out",
             "ufw allow 22/tcp"),
            ("Enable the firewall and check the verbose status",
             "ufw --force enable && ufw status verbose"),
            ("Add a source-restricted rule: MySQL only from 10.0.0.0/8",
             "ufw allow from 10.0.0.0/8 to any port 3306 proto tcp"),
            ("List rules numbered, then delete rule 1",
             "ufw status numbered && ufw delete 1"),
            ("Disable the firewall when done", "ufw disable"),
        ],
        test="ufw status verbose shows Default: deny (incoming), allow (outgoing) plus your 22/tcp and 3306 rules; iptables -L shows the same rules generated underneath.",
        troubleshoot=[
            ("Locked out of SSH",
             "Always allow 22/tcp before ufw enable; from the console run ufw disable, re-add the rule, re-enable"),
            ("Rule never matches",
             "Check order with ufw status numbered - more specific source rules must sit above broad ones"),
            ("ufw: command not found",
             "Install it first: apt update && apt install -y ufw"),
        ],
    ),
    dict(
        num=22,
        topic=4,
        title="TLS Certificate with OpenSSL and Nginx",
        objective="Generate a self-signed X.509 certificate, serve HTTPS from nginx and inspect the TLS handshake.",
        desc="Create an RSA-2048 self-signed certificate with openssl req -x509, configure nginx for HTTPS on 443, then verify the handshake and certificate fields from the client with curl, openssl x509 and s_client.",
        build="An HTTPS server on 443 presenting your own certificate, plus a client-side view of the TLS 1.3 handshake.",
        services="openssl, nginx, curl",
        steps=[
            ("Install the packages", "apt update && apt install -y openssl nginx curl"),
            ("Generate a self-signed RSA-2048 cert and key (add -days 365 for one year)",
             "openssl req -x509 -newkey rsa:2048 -nodes -keyout lab.key -out lab.crt -subj /CN=lab.local"),
            ("Point nginx at the cert and key (listen 443 ssl) and restart",
             "systemctl restart nginx"),
            ("Test the TLS handshake from the client (-k accepts self-signed)",
             "curl -kv https://localhost 2>&1 | head -30"),
            ("Inspect the certificate: Issuer, Subject, validity, public key",
             "openssl x509 -in lab.crt -noout -text | head -20"),
            ("Probe the live handshake with s_client",
             "echo | openssl s_client -connect localhost:443 -servername lab.local 2>/dev/null | head -20"),
        ],
        test="curl -kv https://localhost prints the TLS version, cipher suite and the CN=lab.local certificate; openssl x509 -text shows identical Issuer and Subject - the mark of a self-signed cert.",
        troubleshoot=[
            ("curl: SSL certificate problem",
             "Expected for self-signed - pass -k to curl, or install a CA-signed certificate instead"),
            ("nginx fails to restart",
             "Run nginx -t to locate the config error; verify the ssl_certificate and key paths exist"),
            ("Nothing listening on 443",
             "Confirm listen 443 ssl in the server block, then check with ss -tlnp | grep 443"),
        ],
    ),
    dict(
        num=23,
        topic=4,
        title="SSH Hardening with Key Authentication",
        objective="Harden SSH: Ed25519 key authentication, password login disabled, config validated before reload.",
        desc="Generate an Ed25519 key pair, install the public key in authorized_keys, prove key login works, then disable PasswordAuthentication in sshd_config, validate with sshd -t and confirm password login is refused.",
        build="An SSH daemon that accepts only public-key authentication, with root password login prohibited.",
        services="openssh-server, openssh-client, ssh-keygen",
        steps=[
            ("Generate an Ed25519 key pair (modern elliptic-curve algorithm)",
             "ssh-keygen -t ed25519 -N '' -f ~/.ssh/lab_ed25519"),
            ("Install the public key as authorised and lock down permissions",
             "cat ~/.ssh/lab_ed25519.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"),
            ("Test key-based login - no password prompt should appear",
             "ssh -i ~/.ssh/lab_ed25519 -o StrictHostKeyChecking=no root@localhost whoami"),
            ("Disable password authentication in sshd_config",
             "sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config"),
            ("Validate the config, then reload - never reload untested",
             "sshd -t && systemctl reload ssh"),
            ("Verify password login is now refused",
             "ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@localhost"),
            ("Discuss bonus hardening: Port 2222, AllowUsers, MaxAuthTries 3, fail2ban", ""),
        ],
        test="Key login returns root with no password prompt; forcing password authentication returns Permission denied (publickey).",
        troubleshoot=[
            ("Permission denied with the key",
             "Fix permissions: chmod 700 ~/.ssh and chmod 600 ~/.ssh/authorized_keys - sshd refuses lax modes"),
            ("sshd -t reports errors",
             "Fix the reported line in /etc/ssh/sshd_config before reloading - a bad config can lock you out"),
            ("Password login still works",
             "Check override files in /etc/ssh/sshd_config.d/ for PasswordAuthentication yes, then reload ssh"),
        ],
    ),
    dict(
        num=24,
        topic=4,
        title="Site-to-Site VPN with WireGuard",
        objective="Build a site-to-site WireGuard tunnel between two network namespaces and verify the handshake.",
        desc="Create two namespaces as VPN endpoints, generate Curve25519 key pairs, configure wg0 interfaces with peer public keys and allowed-ips, bring the tunnel up, ping across it and inspect handshake state with wg show.",
        build="An encrypted point-to-point tunnel (10.99.0.1 <-> 10.99.0.2) between two namespaces acting as two sites.",
        services="wireguard, wireguard-tools, iproute2",
        steps=[
            ("Install WireGuard", "apt update && apt install -y wireguard wireguard-tools"),
            ("Create two namespaces representing the two sites",
             "ip netns add site-a && ip netns add site-b"),
            ("Generate a key pair for each peer (repeat for b.key/b.pub)",
             "wg genkey | tee a.key | wg pubkey > a.pub"),
            ("Create a wg0 WireGuard interface in each namespace",
             "ip -n site-a link add wg0 type wireguard"),
            ("Assign the tunnel addresses 10.99.0.1/24 and 10.99.0.2/24",
             "ip -n site-a addr add 10.99.0.1/24 dev wg0"),
            ("Set private key, listen port and peer allowed-ips on both sides",
             "ip netns exec site-a wg set wg0 private-key /tmp/a.key listen-port 51820"),
            ("Bring both tunnel interfaces up",
             "ip -n site-a link set wg0 up && ip -n site-b link set wg0 up"),
            ("Ping site-a across the encrypted tunnel from site-b",
             "ip netns exec site-b ping -c2 10.99.0.1"),
            ("Inspect the peer public key, last handshake and byte counters",
             "ip netns exec site-a wg show"),
            ("Clean up namespaces and key files",
             "ip netns del site-a && ip netns del site-b"),
        ],
        test="ping -c2 10.99.0.1 from site-b succeeds through the tunnel; wg show reports the peer public key, a recent handshake time and rising transfer counters.",
        troubleshoot=[
            ("Ping fails across the tunnel",
             "Check wg show for a handshake; verify each peer entry uses the other side's PUBLIC key"),
            ("wg show shows no handshake",
             "Confirm site-b's endpoint 127.0.0.1:51820 matches site-a's listen-port, and allowed-ips cover the peer /32"),
            ("wg0 already exists",
             "Stale run - delete with ip netns del site-a && ip netns del site-b and recreate"),
        ],
    ),
    dict(
        num=25,
        topic=4,
        title="Port Scanning and Service Hardening",
        objective="Enumerate exposed services with nmap and reduce the attack surface by disabling what is unneeded.",
        desc="SYN-scan all 65535 TCP ports on your own host, identify service versions and the OS, cross-check each open port against ss -tulnp, disable an unnecessary service and re-scan to confirm the port is closed.",
        build="A port-by-port inventory of your host's attack surface, with an unneeded service disabled and verified closed.",
        services="nmap, ss, systemctl",
        steps=[
            ("Install nmap", "apt update && apt install -y nmap"),
            ("SYN-scan (half-open, -sS) all 65535 TCP ports on localhost",
             "nmap -sS -p- 127.0.0.1"),
            ("Enumerate service versions (-sV probes banners) on key ports",
             "nmap -sV -p 22,80,443 127.0.0.1"),
            ("Fingerprint the operating system (requires root)",
             "nmap -O 127.0.0.1"),
            ("Cross-check every open port against its owning process",
             "ss -tulnp"),
            ("Disable an unneeded service - ask: do I need this running?",
             "systemctl disable --now apache2"),
            ("Re-scan to confirm the port is now closed",
             "nmap -sS -p 80 127.0.0.1"),
        ],
        test="The final nmap -sS -p 80 scan reports the port closed, and ss -tulnp no longer lists the disabled service - the attack surface measurably shrank.",
        troubleshoot=[
            ("Scan takes very long",
             "-p- probes 65535 ports; in the lab scan a shortlist such as -p 1-1024 instead"),
            ("nmap -O gives no result",
             "OS fingerprinting needs root privileges and at least one open and one closed port"),
            ("Port still open after disable",
             "Another process owns it - find the PID with ss -tulnp and stop that unit too"),
        ],
    ),
    dict(
        num=26,
        topic=4,
        title="Intrusion Detection with Suricata",
        objective="Run Suricata as an IDS, trigger a known signature and read the alert in fast.log and eve.json.",
        desc="Install Suricata, pull the Emerging Threats ruleset, start the engine on eth0, generate benign trigger traffic from testmynids.org, then trace the resulting alert through fast.log and the JSON eve.json event stream.",
        build="A live IDS on eth0 with a current ET ruleset, plus a captured alert you can parse as JSON with jq.",
        services="suricata, suricata-update, jq, curl, TIS Cybersecurity Simulator",
        steps=[
            ("Install Suricata and jq", "apt update && apt install -y suricata jq"),
            ("Update the Emerging Threats community ruleset", "suricata-update"),
            ("Start Suricata as a daemon (-D) on the active interface",
             "suricata -i eth0 -D"),
            ("Confirm the engine started cleanly",
             "tail /var/log/suricata/suricata.log"),
            ("Trigger a well-known test signature via the NIDS test page",
             "curl -s http://testmynids.org/uid/index.html >/dev/null"),
            ("Inspect the alert in the human-readable fast.log",
             "tail /var/log/suricata/fast.log"),
            ("Filter the same alert from the eve.json event stream with jq",
             "cat /var/log/suricata/eve.json | jq 'select(.event_type==\"alert\")' | head -20"),
            ("Run the TIS Cybersecurity Simulator network-attack scenarios to see IDS traffic patterns",
             ""),
            ("Stop Suricata", "pkill suricata"),
        ],
        test="fast.log shows an alert like GPL ATTACK_RESPONSE id check returned root; filtering eve.json for event_type alert returns the same event with src/dest IPs and severity.",
        troubleshoot=[
            ("No alerts appear",
             "Confirm Suricata listens on the right interface (check ip a), then re-run the testmynids curl"),
            ("suricata-update fails",
             "Check Internet access - the rules download from the Emerging Threats feed"),
            ("eve.json is empty",
             "Give the engine a few seconds after the trigger; check suricata.log for startup errors"),
        ],
    ),
    dict(
        num=27,
        topic=4,
        title="Building an ACL with iptables",
        objective="Build an ordered iptables ACL that permits MySQL from one subnet and drops it from everywhere else.",
        desc="Insert an ACCEPT rule for TCP 3306 from 10.0.0.0/24 above an appended DROP, verify ordering with --line-numbers, test both paths with nc from allowed and blocked sources, then persist the rules across reboots.",
        build="A working two-rule ACL on the INPUT chain proving top-down, first-match evaluation, saved to survive reboot.",
        services="iptables, netcat, iptables-persistent",
        steps=[
            ("Inspect the current INPUT chain (default policy is ACCEPT)",
             "iptables -L INPUT -n -v --line-numbers"),
            ("Insert (-I, at the top) an ACCEPT for MySQL from 10.0.0.0/24",
             "iptables -I INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT"),
            ("Append (-A, at the bottom) a DROP for MySQL from everywhere else",
             "iptables -A INPUT -p tcp --dport 3306 -j DROP"),
            ("Verify ordering - the ACCEPT must sit above the DROP",
             "iptables -L INPUT -n -v --line-numbers"),
            ("Test from a blocked source: the DROP swallows the probe",
             "nc -zv 127.0.0.1 3306"),
            ("Add an allowed source address and retest from it",
             "ip addr add 10.0.0.5/24 dev lo && nc -zv -s 10.0.0.5 127.0.0.1 3306"),
            ("Persist the rules so they survive reboot",
             "apt install -y iptables-persistent && netfilter-persistent save"),
            ("Clean up: delete both rules and the extra address",
             "iptables -D INPUT -p tcp --dport 3306 -j DROP"),
        ],
        test="The probe from a blocked source hangs (dropped); the probe from 10.0.0.5 gets an instant refused/RST - accepted by the ACL, nothing listening. The filter demonstrably works.",
        troubleshoot=[
            ("ACL never blocks anything",
             "The ACCEPT may sit below the DROP - first match wins; verify order with --line-numbers"),
            ("Rules vanish after reboot",
             "Install iptables-persistent and run netfilter-persistent save to write /etc/iptables/rules.v4"),
            ("nc test looks inconclusive",
             "With no MySQL listening, allowed sources see instant RST (refused); dropped sources see a timeout"),
        ],
    ),
]


CONTENT4 = [
    # ================================================================
    # Security fundamentals: CIA, terminology, compliance  (OBJ 4.1)
    # ================================================================
    dict(type="big",
         line1="Domain 4 - Network Security.",
         line2="14% of the exam: encryption, identity, attacks, hardening, segmentation and physical defence - how we keep the network confidential, intact and available.",
         kicker="DOMAIN 4 · 14% OF THE EXAM", color="blue"),

    dict(type="cards", title="The CIA Triad",
         kicker="OBJ 4.1 · SECURITY CONCEPTS",
         cards=[
             ("blue", "Confidentiality", [
                 "Only authorised eyes see the data",
                 "Encryption in transit and at rest",
                 "Access controls and least privilege"]),
             ("teal", "Integrity", [
                 "Data arrives exactly as it was sent",
                 "Hashes detect tampering (SHA-256)",
                 "Digital signatures prove the origin"]),
             ("violet", "Availability", [
                 "Systems stay reachable when needed",
                 "Redundancy, backups, DDoS defence",
                 "Balance security against usability"]),
         ]),

    dict(type="tiles", title="Security Terminology",
         kicker="OBJ 4.1 · SECURITY TERMINOLOGY", cols=2, accent="blue",
         items=[
             ("Threat", "Any actor or event with the potential to harm the network - from a ransomware crew to a burst pipe above the server room."),
             ("Vulnerability", "A weakness that could be abused - an unpatched service, a default password, an open port nobody remembers."),
             ("Exploit", "The technique or code that weaponises a vulnerability to gain access or disrupt service."),
             ("Risk", "Likelihood times impact of a threat exploiting a vulnerability - what budgets and priorities are set against."),
             ("CVE", "Common Vulnerabilities and Exposures - the public catalogue of disclosed flaws, each with an ID like CVE-2021-44228 (Log4Shell)."),
             ("Zero-day", "A flaw attackers find before the vendor does - no patch exists yet, so layered defence is the only cover."),
         ]),

    dict(type="process", title="From Threat to Impact",
         kicker="OBJ 4.1 · SECURITY TERMINOLOGY", color="amber",
         stages=[
             ("Threat", "actor with intent"),
             ("Vulnerability", "a weakness exposed"),
             ("Exploit", "the flaw weaponised"),
             ("Breach", "access gained"),
             ("Impact", "CIA compromised"),
         ],
         synthesis=("WHY IT MATTERS",
                    "Break any link and the attack fails - patching removes vulnerabilities, hardening blocks exploits, monitoring and response limit impact.")),

    dict(type="tiles", title="Audits and Regulatory Compliance",
         kicker="OBJ 4.1 · AUDITS & COMPLIANCE", cols=2, accent="teal",
         items=[
             ("Security audit", "An independent check that controls exist and work - configs, logs, access reviews, penetration tests."),
             ("Data locality", "Laws that dictate WHERE data may be stored and processed - pins your cloud regions and backup sites."),
             ("PCI DSS", "Card-industry standard: anyone storing or transmitting card data must segment, encrypt and log that environment."),
             ("GDPR", "EU personal-data regulation: privacy by design, breach notification within 72 hours, heavy fines for leaks."),
         ]),

    dict(type="table", title="Compliance Regimes at a Glance",
         kicker="OBJ 4.1 · AUDITS & COMPLIANCE", accent="teal",
         headers=["Regime", "Scope", "Network requirement"],
         rows=[
             ["PCI DSS", "Cardholder data environments", "Segment the CDE, encrypt, log all access"],
             ["GDPR", "Personal data of EU residents", "Protect by design; report breaches fast"],
             ["Data locality", "Where data may physically live", "Keep regulated data in approved regions"],
             ["PDPA (SG)", "Singapore personal data", "Reasonable security arrangements required"],
         ],
         note="Audits verify these on paper AND on the wire - segmentation and logs are the evidence."),

    # ================================================================
    # Zones, defense in depth, firewalls  (OBJ 4.3)  -> LAB 21
    # ================================================================
    dict(type="tiles", title="Defense in Depth",
         kicker="OBJ 4.3 · DEFENSE TECHNIQUES", cols=2, accent="blue",
         items=[
             ("Perimeter", "Edge firewalls, screened subnet, DDoS scrubbing - the first line, never the only line."),
             ("Network", "Segmentation, VLANs, ACLs, IDS/IPS - contain whatever gets past the edge."),
             ("Host / endpoint", "Host firewalls, EDR, patching, hardening - every machine defends itself."),
             ("Application", "Input validation, secure APIs, WAF - the layer attackers actually talk to."),
             ("Data", "Encryption at rest, backups, DLP - the final prize gets its own armour."),
             ("Separation of duties", "No single person holds enough rights to abuse the system alone."),
         ]),

    dict(type="two_col", title="Trusted vs Untrusted Zones",
         kicker="OBJ 4.3 · ZONES",
         lhead="Trusted zone", rhead="Untrusted / screened",
         left=[
             "Internal LANs and data-centre subnets",
             "Users and devices are authenticated",
             "Servers holding business data",
             "Still segmented - trust is never absolute",
         ],
         right=[
             "The Internet - assume hostile",
             "Guest and BYOD networks",
             "Screened subnet (DMZ) for public services",
             "Traffic crossing zones must pass a firewall",
         ]),

    dict(type="tiles", title="The Screened Subnet (DMZ)",
         kicker="OBJ 4.3 · SCREENED SUBNET", cols=2, accent="violet",
         items=[
             ("Screened subnet", "A buffer network between Internet and LAN hosting the public-facing servers - web, mail, DNS."),
             ("Bastion host", "Any machine directly exposed to the Internet - hardened to the maximum, expected to be attacked."),
             ("Two-firewall design", "Internet -> outer firewall -> DMZ -> inner firewall -> LAN; a DMZ breach still faces a wall."),
             ("Why it works", "If a public server is compromised, the attacker is contained in the DMZ - not inside your LAN."),
         ]),

    dict(type="tiles", title="Firewall Families",
         kicker="OBJ 4.3 · FIREWALLS", cols=2, accent="blue",
         items=[
             ("Network firewall", "A dedicated device at zone boundaries filtering traffic for the whole network."),
             ("Host-based firewall", "Software on each machine (ufw, Windows Defender FW) - the last line, per host."),
             ("Hardware vs software", "Physical appliances at the edge; virtual/software firewalls in cloud and hosts."),
             ("UTM / NGFW", "Unified threat management bundles firewall, IPS, AV and URL filtering in one box."),
         ]),

    dict(type="table", title="Stateless, Stateful, Application-Aware",
         kicker="OBJ 4.3 · FIREWALLS", accent="blue",
         headers=["Type", "Decides on", "Strength", "Limit"],
         rows=[
             ["Stateless", "Ports + IPs, per packet (ACL)", "Fast, simple, cheap", "No conversation context"],
             ["Stateful", "Tracks connection state", "Return traffic auto-allowed", "More CPU and memory"],
             ["App-aware (NGFW)", "Packet content via DPI", "Sees apps inside port 443", "Costly; TLS inspection"],
         ],
         note="Most modern firewalls combine all three - ACL speed plus stateful context plus DPI."),

    dict(type="big",
         line1="Default deny. Allow by exception.",
         line2="A firewall policy starts by blocking everything inbound, then permits only the specific ports, sources and services the business needs - the stance you build in Lab 21.",
         kicker="OBJ 4.3 · THE GOLDEN RULE", color="blue"),

    dict(type="lab", num=21),

    # ================================================================
    # Encryption, hashes, TLS, PKI  (OBJ 4.1)  -> LAB 22
    # ================================================================
    dict(type="big",
         line1="Making TCP/IP secure.",
         line2="TCP/IP was designed for openness, not secrecy - confidentiality, integrity and availability are bolted on with encryption, hashes and authentication at every layer.",
         kicker="OBJ 4.1 · LOGICAL SECURITY", color="teal"),

    dict(type="two_col", title="Encryption: In Transit vs At Rest",
         kicker="OBJ 4.1 · ENCRYPTION",
         lhead="Data in transit", rhead="Data at rest",
         left=[
             "Moving across the network",
             "TLS 1.3 for web and APIs",
             "IPSec or WireGuard for site links",
             "SSH for management sessions",
         ],
         right=[
             "Stored on disk or in the cloud",
             "Full-disk encryption (LUKS, BitLocker)",
             "Database and object-store encryption",
             "Key management decides real safety",
         ]),

    dict(type="tiles", title="Symmetric Encryption",
         kicker="OBJ 4.1 · ENCRYPTION", cols=2, accent="teal",
         items=[
             ("Cleartext", "Any unencrypted data - readable by whoever captures the packet."),
             ("Algorithm + key", "The algorithm (AES) is public and well studied; all the secrecy lives in the key."),
             ("Ciphertext", "The scrambled output - useless to an eavesdropper without the key."),
             ("Same key both ways", "Symmetric = one shared key encrypts AND decrypts - fast, but that key must travel safely."),
         ]),

    dict(type="table", title="Symmetric vs Asymmetric Encryption",
         kicker="OBJ 4.1 · ENCRYPTION", accent="teal",
         headers=["", "Symmetric", "Asymmetric"],
         rows=[
             ["Keys", "One shared secret key", "Public + private key pair"],
             ["Speed", "Fast - bulk data encryption", "Slow - small payloads only"],
             ["Examples", "AES-256, ChaCha20", "RSA-2048, ECC / Curve25519"],
             ["Key exchange", "Hard - secret must travel", "Easy - publish the public key"],
             ["Used for", "Session data after handshake", "Handshake, signatures, certs"],
         ],
         note="TLS uses both: asymmetric crypto agrees a session key, symmetric crypto carries the data."),

    dict(type="tiles", title="Cryptographic Hashes",
         kicker="OBJ 4.1 · INTEGRITY", cols=2, accent="violet",
         items=[
             ("Fixed-size fingerprint", "Any input, one fixed-length output - SHA-256 always yields 256 bits."),
             ("Integrity, not secrecy", "A hash proves data is unchanged; it does not hide the data."),
             ("Avalanche effect", "Change one bit of input and the entire hash changes - tampering is obvious."),
             ("MD5 / SHA-1 retired", "Collisions have been engineered - use SHA-256 or SHA-3 today."),
             ("Password storage", "Servers store salted hashes, never the password itself."),
             ("HMAC", "A keyed hash proving both integrity and authenticity of a message."),
         ]),

    dict(type="process", title="The TLS 1.3 Handshake",
         kicker="OBJ 4.1 · TLS", color="teal",
         stages=[
             ("ClientHello", "ciphers + key share"),
             ("ServerHello", "key share + cert"),
             ("Verify certificate", "chain to trusted CA"),
             ("Derive session keys", "both sides compute"),
             ("Encrypted data", "symmetric AES/ChaCha"),
         ],
         synthesis=("WHY IT MATTERS",
                    "TLS 1.3 completes in one round-trip: asymmetric crypto authenticates the server and agrees keys, then fast symmetric crypto protects the whole session.")),

    dict(type="tiles", title="Certificates and PKI",
         kicker="OBJ 4.1 · PKI", cols=2, accent="blue",
         items=[
             ("X.509 certificate", "Binds a public key to an identity (CN/SAN), signed by an issuer with validity dates."),
             ("Certificate authority", "A trusted third party that signs certificates after verifying the requester's identity."),
             ("Chain of trust", "Leaf cert -> intermediate CA -> root CA pre-installed in every OS and browser."),
             ("Self-signed", "Signed by its own key - fine for labs and internal tools, but every browser warns."),
             ("CSR", "Certificate signing request - your public key plus identity, sent to the CA for signing."),
             ("Let's Encrypt / ACME", "Free automated CA - the ACME protocol issues and renews certs every 90 days."),
         ]),

    dict(type="worked", title="Reading a Certificate with openssl x509",
         kicker="OBJ 4.1 · CERTIFICATES",
         intro="The certificate you generate in Lab 22, decoded field by field.",
         code=[
             "$ openssl x509 -in lab.crt -noout -text",
             "Certificate:",
             "  Data:",
             "    Serial Number: 5d:9c:41:...:2e",
             "    Issuer: CN = lab.local",
             "    Validity",
             "      Not Before: Aug 19 02:00:00 2026 GMT",
             "      Not After : Aug 19 02:00:00 2027 GMT",
             "    Subject: CN = lab.local",
             "    Subject Public Key Info:",
             "      Public-Key: (2048 bit)",
         ],
         explain=[
             ("Issuer = Subject", "Both read CN=lab.local - the certificate signed itself, so no browser will trust it."),
             ("Validity window", "Outside Not Before / Not After the cert throws expired or not-yet-valid errors."),
             ("Public key", "The RSA-2048 key clients use in the TLS handshake to agree session secrets."),
         ]),

    dict(type="tiles", title="Certificate Error Scenarios",
         kicker="OBJ 4.1 · CERTIFICATES", cols=2, accent="amber",
         items=[
             ("Self-signed warning", "No CA in the chain - the browser shows ERR_CERT_AUTHORITY_INVALID."),
             ("Expired certificate", "Past its Not After date - renew with the issuer; automate renewal with ACME."),
             ("Name mismatch", "The CN/SAN does not match the URL's hostname - common after renames and moves."),
             ("Revoked certificate", "The CA withdrew it - clients check live via OCSP or download CRL lists."),
         ]),

    dict(type="lab", num=22),

    # ================================================================
    # IAM, MFA, access control, AAA protocols, hardening  -> LAB 23
    # ================================================================
    dict(type="big",
         line1="Who are you, and what may you do?",
         line2="Identity and access management is security's control plane: identification, authentication, authorization and accounting govern every login, port and API call.",
         kicker="OBJ 4.1 · IAM", color="violet"),

    dict(type="flow", title="Identification to Accounting (IAM / AAA)",
         kicker="OBJ 4.1 · IAM", color="violet",
         steps=[
             "Identification - claim an identity (username)",
             "Authentication - prove it (password + MFA)",
             "Authorization - what you may do (RBAC)",
             "Accounting - log what you did (audit trail)",
         ]),

    dict(type="tiles", title="Multifactor Authentication (MFA)",
         kicker="OBJ 4.1 · MFA", cols=2, accent="violet",
         items=[
             ("Something you know", "Password, PIN, passphrase - the weakest factor on its own."),
             ("Something you have", "Phone TOTP app, smart card, hardware token (YubiKey)."),
             ("Something you are", "Biometrics - fingerprint, face, iris."),
             ("Somewhere you are", "Location attribute - geofencing blocks logins from outside approved areas."),
             ("Something you do", "Behavioural attributes - typing rhythm, signature dynamics."),
             ("MFA = 2+ DIFFERENT factors", "Two passwords is not MFA; a password plus a TOTP code is."),
         ]),

    dict(type="tiles", title="Time-Based and Location-Based Authentication",
         kicker="OBJ 4.1 · MFA", cols=2, accent="teal",
         items=[
             ("Time-based OTP (TOTP)", "A shared secret plus the current time yields a 6-digit code valid for 30 seconds."),
             ("Geofencing", "Access permitted only from defined geographic areas or IP ranges."),
             ("Push / passkeys", "FIDO2 passkeys bind the login to the genuine site - phishing-resistant MFA."),
             ("Least privilege", "Grant the minimum rights a role needs, and remove them when the role ends."),
         ]),

    dict(type="tiles", title="Access Control Models",
         kicker="OBJ 4.1 · AUTHORIZATION", cols=2, accent="blue",
         items=[
             ("Role-based (RBAC)", "Rights attach to roles/groups; users inherit by membership - the enterprise default."),
             ("Mandatory (MAC)", "Labels and clearances fixed by policy; users cannot re-share - military and government."),
             ("Discretionary (DAC)", "The resource owner decides who gets access - flexible, but permissions sprawl."),
             ("Least privilege lens", "Whatever the model, grant minimum rights and review them regularly."),
         ]),

    dict(type="tiles", title="Single Sign-On and Federation",
         kicker="OBJ 4.1 · SSO", cols=2, accent="violet",
         items=[
             ("Single sign-on (SSO)", "Authenticate once, access many apps - one strong login to protect with MFA."),
             ("SAML", "XML federation: an identity provider (IdP) asserts who you are to service providers."),
             ("LDAP / LDAPS", "Directory lookups on TCP 389; LDAPS wraps them in TLS on 636 - how apps query AD."),
             ("Kerberos", "Ticket-based SSO in Windows domains - time-stamped tickets issued by the KDC."),
         ]),

    dict(type="table", title="RADIUS vs TACACS+",
         kicker="OBJ 4.1 · AAA PROTOCOLS", accent="violet",
         headers=["", "RADIUS", "TACACS+"],
         rows=[
             ["Transport", "UDP 1812/1813 (or 1645/1646)", "TCP 49"],
             ["Encryption", "Password field only", "Entire payload"],
             ["AAA split", "AuthN + AuthZ combined", "All three separated"],
             ["Typical use", "Wi-Fi, VPN, 802.1X access", "Admin access to network gear"],
             ["Origin", "Open standard", "Cisco (now published)"],
         ],
         note="Exam favourite: RADIUS = network access over UDP; TACACS+ = device administration over TCP 49."),

    dict(type="tiles", title="EAP - the Authentication Framework",
         kicker="OBJ 4.1 · EAP", cols=2, accent="teal",
         items=[
             ("EAP", "A framework, not one protocol - it carries many authentication methods inside 802.1X."),
             ("EAP-TLS", "Certificates on both server and client - strongest, passwordless."),
             ("PEAP", "The server's cert builds a TLS tunnel, credentials go inside - the campus Wi-Fi standard."),
             ("EAP-PSK / EAP-MD5", "Legacy lightweight methods - avoid wherever certificates are possible."),
         ]),

    dict(type="tiles", title="Device Hardening",
         kicker="OBJ 4.3 · DEVICE HARDENING", cols=2, accent="blue",
         items=[
             ("Change default passwords", "Factory admin credentials sit in every attacker's wordlist - change them on day one."),
             ("Disable unused services", "Every listening daemon is attack surface - if nobody needs it, stop and disable it."),
             ("Disable unused ports", "Shut idle switch ports; an unused wall jack must not be a live network drop."),
             ("Patch firmware", "Known CVEs in network gear are scanned for within hours of disclosure."),
             ("Key management", "Rotate SSH and API keys; revoke a leaver's keys the day they leave."),
             ("Secure the management plane", "SSH not Telnet, HTTPS not HTTP, on a dedicated management VLAN."),
         ]),

    dict(type="worked", title="A Hardened sshd_config",
         kicker="OBJ 4.3 · HARDENING IN PRACTICE",
         intro="The Lab 23 end-state: keys only, limited users, tested before reload.",
         code=[
             "# /etc/ssh/sshd_config - hardened",
             "Port 2222",
             "PermitRootLogin prohibit-password",
             "PasswordAuthentication no",
             "PubkeyAuthentication yes",
             "MaxAuthTries 3",
             "AllowUsers admin",
             "",
             "# validate BEFORE reloading:",
             "$ sshd -t && systemctl reload ssh",
         ],
         explain=[
             ("Keys only", "PasswordAuthentication no removes brute force as an attack class - keys cannot be guessed."),
             ("Blast-radius limits", "AllowUsers and MaxAuthTries shrink who may try to log in, and how often."),
             ("sshd -t", "Test the config before reload - a syntax error must never lock you out of a remote box."),
         ]),

    dict(type="lab", num=23),

    # ================================================================
    # VPN / encryption in transit  -> LAB 24
    # ================================================================
    dict(type="tiles", title="VPN - Extending the Trusted Zone",
         kicker="OBJ 4.1 · ENCRYPTION IN TRANSIT", cols=2, accent="teal",
         items=[
             ("Site-to-site VPN", "Routers or firewalls tunnel whole networks together across the Internet."),
             ("Client-to-site", "Remote access - a laptop joins the corporate network from anywhere."),
             ("IPSec", "AH/ESP with IKE key exchange - the classic standard: rich, interoperable, complex."),
             ("WireGuard", "Modern and tiny: Curve25519 key pairs, no PKI needed - what you build in Lab 24."),
             ("Split vs full tunnel", "Route everything through the VPN, or only the corporate subnets."),
             ("Why it matters", "A VPN extends the trusted zone across an untrusted network - encryption in transit."),
         ]),

    dict(type="table", title="VPN Technologies Compared",
         kicker="OBJ 4.1 · ENCRYPTION IN TRANSIT", accent="teal",
         headers=["", "IPSec", "TLS VPN", "WireGuard"],
         rows=[
             ["Layer", "Network (L3)", "Session (TLS)", "Network (L3)"],
             ["Keys", "IKE + certs / PSK", "X.509 certificates", "Static 32-byte key pairs"],
             ["Codebase", "Large, complex", "Large (OpenVPN)", "Tiny (~4k lines)"],
             ["Speed", "Good (HW offload)", "Moderate", "Excellent"],
             ["Best for", "Standards, site-to-site", "Remote access via 443", "Modern deployments"],
         ],
         note="WireGuard's allowed-ips doubles as a routing rule AND an inbound ACL - you will see this in Lab 24."),

    dict(type="lab", num=24),

    # ================================================================
    # Attack surface, malware, social engineering  -> LAB 25
    # ================================================================
    dict(type="big",
         line1="Every open port is a doorway.",
         line2="Attack-surface reduction is the cheapest security win: enumerate what is listening, ask why it is there, and disable what nobody needs - before an attacker does the asking.",
         kicker="OBJ 4.3 · ATTACK SURFACE", color="amber"),

    dict(type="tiles", title="Malware Taxonomy",
         kicker="OBJ 4.2 · MALWARE", cols=2, accent="amber",
         items=[
             ("Virus / worm", "A virus infects files; a worm self-propagates across the network unaided."),
             ("Trojan / RAT", "Hides inside legitimate-looking software; a RAT hands the attacker remote control."),
             ("Ransomware", "Encrypts your data and demands payment - today's top business threat."),
             ("Spyware / keylogger", "Silently collects keystrokes, credentials and screen contents."),
             ("Rootkit", "Buries itself under the OS to hide processes and survive detection."),
             ("Logic bomb", "Dormant code that triggers on a date or event - often an insider plant."),
         ]),

    dict(type="tiles", title="Social Engineering",
         kicker="OBJ 4.2 · SOCIAL ENGINEERING", cols=2, accent="amber",
         items=[
             ("Phishing", "Fraudulent mail and sites harvest credentials; spear phishing targets a person, whaling an exec."),
             ("Dumpster diving", "Discarded printouts leak configs and passwords - shred everything."),
             ("Shoulder surfing", "Watching screens and keypads - privacy filters and awareness defeat it."),
             ("Tailgating", "Following a badge-holder through a secure door - vestibules stop it."),
             ("Impersonation", "The fake IT-support call that just needs your password to help you."),
             ("Defence = education", "Humans are part of the perimeter: train, phish-test, make reporting easy."),
         ]),

    dict(type="tiles", title="Password Attacks",
         kicker="OBJ 4.2 · PASSWORD ATTACKS", cols=2, accent="grey",
         items=[
             ("Brute force", "Try every combination - length beats complexity; each extra character multiplies the work."),
             ("Dictionary", "Try likely words and leaked passwords first - most humans are predictable."),
             ("Credential stuffing", "Replay leaked username/password pairs on other sites - MFA breaks it."),
             ("Defences", "Long passphrases, lockout policies, salted hashes, MFA everywhere."),
         ]),

    dict(type="flow", title="Vulnerability Management Loop",
         kicker="OBJ 4.3 · ATTACK SURFACE", color="amber",
         steps=[
             "Scan the estate for exposed services",
             "Prioritise by CVSS score and exploitability",
             "Patch on a defined cadence with change control",
             "Re-scan to verify the exposure is closed",
         ]),

    dict(type="lab", num=25),

    # ================================================================
    # Network attacks, hardening, NAC, segmentation, IDS  -> LAB 26
    # ================================================================
    dict(type="table", title="Attack Catalogue: Vector, Layer, Defence",
         kicker="OBJ 4.2 · TYPES OF ATTACKS", accent="amber",
         headers=["Attack", "Layer", "How it works", "Primary defence"],
         rows=[
             ["DoS / DDoS", "3-7", "Botnet floods links or servers", "Scrubbing, rate limits"],
             ["MAC flooding", "2", "Overflow CAM table; switch floods", "Port security limits"],
             ["ARP poisoning", "2", "Forged replies put attacker on-path", "Dynamic ARP Inspection"],
             ["VLAN hopping", "2", "Double tags / fake trunk cross VLANs", "No native VLAN, no DTP"],
             ["DNS poisoning", "7", "Fake records redirect victims", "DNSSEC, patched resolvers"],
             ["Evil twin", "1-2", "Cloned SSID captures clients", "802.1X, WIPS monitoring"],
         ],
         note="For every attack, know the layer it lives at - the defence always sits at the same layer."),

    dict(type="tiles", title="DoS and DDoS in Depth",
         kicker="OBJ 4.2 · DoS/DDoS", cols=2, accent="amber",
         items=[
             ("Botnet and C2", "Compromised zombies take orders from a command-and-control server."),
             ("Volumetric", "Saturate the pipe - UDP floods, amplification via open DNS/NTP servers."),
             ("Protocol attack", "Exhaust state tables - SYN floods hold thousands of half-open connections."),
             ("Application attack", "Cheap requests, expensive responses - HTTP floods and Slowloris."),
         ]),

    dict(type="process", title="Anatomy of an ARP Poisoning Attack",
         kicker="OBJ 4.2 · ON-PATH ATTACKS", color="amber",
         stages=[
             ("Recon", "attacker joins the LAN"),
             ("Poison", "forged ARP replies sent"),
             ("On-path", "victim traffic redirected"),
             ("Harvest", "credentials sniffed"),
             ("Defend", "DAI drops forged ARP"),
         ],
         synthesis=("BREAK THE CHAIN",
                    "Dynamic ARP Inspection validates every ARP reply against the DHCP snooping binding table - forged replies are dropped at the switch port.")),

    dict(type="tiles", title="VLAN Hopping",
         kicker="OBJ 4.2 · VLAN HOPPING", cols=2, accent="violet",
         items=[
             ("Switch spoofing", "The attacker negotiates a trunk via DTP and receives every VLAN - disable DTP, set access mode."),
             ("Double tagging", "Outer tag stripped on the native VLAN, inner tag delivers into the victim VLAN - one-way but real."),
             ("Native VLAN hygiene", "Use a dedicated, unused native VLAN; never carry user traffic on it."),
             ("Private VLANs", "Port isolation stops peer-to-peer traffic even inside the same VLAN."),
         ]),

    dict(type="tiles", title="Rogue Devices and On-Path Attacks",
         kicker="OBJ 4.2 · ROGUE DEVICES", cols=2, accent="amber",
         items=[
             ("Rogue DHCP server", "Hands out attacker-controlled gateway/DNS - a lease outside your network ID is the tell."),
             ("Rogue AP", "An unauthorised access point bridging outsiders straight into the LAN."),
             ("Evil twin", "A cloned corporate SSID; clients auto-join and their traffic is captured."),
             ("On-path (MITM)", "The attacker relays between two parties, reading or altering everything."),
             ("Defence: snooping + 802.1X", "DHCP snooping drops rogue offers; port authentication blocks rogue gear."),
             ("Defence: WIPS", "Wireless IPS detects unknown SSIDs and contains rogue radios."),
         ]),

    dict(type="tiles", title="Spoofing Attacks",
         kicker="OBJ 4.2 · SPOOFING", cols=2, accent="grey",
         items=[
             ("MAC spoofing", "Clone an allowed MAC address to slip past port filters."),
             ("IP spoofing", "Forge the source address - the engine behind amplification DDoS."),
             ("DNS spoofing / poisoning", "Corrupt resolver caches so good names resolve to bad hosts."),
             ("Defences", "Ingress filtering (BCP 38), DNSSEC validation, Dynamic ARP Inspection."),
         ]),

    dict(type="tiles", title="Switch and Network Hardening",
         kicker="OBJ 4.3 · NETWORK HARDENING", cols=2, accent="blue",
         items=[
             ("DHCP snooping", "Only trusted uplink ports may send DHCP offers - kills rogue DHCP."),
             ("Dynamic ARP Inspection", "Validates ARP against the snooping bindings - kills ARP poisoning."),
             ("Port security", "Limit MACs per port, err-disable on violation - kills MAC flooding."),
             ("RA guard", "Blocks rogue IPv6 router advertisements at access ports."),
             ("Control plane policing", "Rate-limits traffic to the device CPU so it survives a DoS."),
             ("Disable unused ports", "A patch-panel jack nobody uses should terminate nowhere."),
         ]),

    dict(type="process", title="802.1X Network Access Control",
         kicker="OBJ 4.3 · NAC", color="blue",
         stages=[
             ("Supplicant", "device asks to join"),
             ("Authenticator", "switch relays EAP"),
             ("RADIUS server", "credentials checked"),
             ("Posture check", "patch level verified"),
             ("VLAN assigned", "access or quarantine"),
         ],
         synthesis=("WHY IT MATTERS",
                    "Nothing gets a usable port until identity and device health are proven - NAC turns every access port and SSID into a checkpoint.")),

    dict(type="table", title="Segmentation Enforcement Zones",
         kicker="OBJ 4.1 · SEGMENTATION", accent="violet",
         headers=["Zone", "What lives there", "Why segregate it"],
         rows=[
             ["IoT", "Cameras, sensors, smart devices", "Rarely patched; assume compromised"],
             ["IIoT / OT", "Industrial sensors, actuators", "Uptime-critical; no direct IT access"],
             ["SCADA / ICS", "Plant supervisory control", "Legacy protocols with no auth"],
             ["Guest", "Visitor phones and laptops", "Internet only - zero internal reach"],
             ["BYOD", "Staff personal devices", "Unmanaged; NAC posture, limited access"],
         ],
         note="Segment by trust and blast radius: a hacked camera must never see the finance VLAN."),

    dict(type="tiles", title="Deception Technologies",
         kicker="OBJ 4.1 · DECEPTION", cols=2, accent="violet",
         items=[
             ("Honeypot", "A deliberately vulnerable decoy host - any touch on it is by definition suspicious."),
             ("Honeynet", "A whole decoy network of honeypots modelling your real estate."),
             ("Why deceive", "Attackers burn time on fakes while defenders harvest indicators and early warning."),
             ("Placement", "In the screened subnet or a dedicated VLAN - never among production data."),
         ]),

    dict(type="decision", title="IDS or IPS - Where Does the Sensor Sit?",
         kicker="OBJ 4.3 · IDS/IPS",
         question="Should the sensor sit inline\nand block, or watch a copy\nand alert?",
         yes=("INLINE - IPS",
              "Sits in the traffic path and drops malicious packets in real time. Risk: a false positive blocks legitimate traffic; adds latency."),
         no=("PASSIVE - IDS",
             "Watches a mirror/TAP copy and raises alerts for analysts. No traffic risk, but detection only - response is manual."),
         note="Suricata can run either mode - Lab 26 runs it passively as an IDS on eth0."),

    dict(type="tiles", title="How IDS/IPS Detect",
         kicker="OBJ 4.3 · IDS/IPS", cols=2, accent="blue",
         items=[
             ("Signature-based", "Match known patterns (ET rules) - precise, but blind to novel attacks."),
             ("Anomaly-based", "Baseline normal, alert on deviation - catches zero-days, more false positives."),
             ("Rule feeds", "Emerging Threats and Snort VRT keep signatures current - update daily."),
             ("Where alerts land", "Suricata writes fast.log for humans and eve.json for SIEM pipelines."),
         ]),

    dict(type="worked", title="Reading a Suricata Alert (eve.json)",
         kicker="OBJ 4.3 · IDS IN PRACTICE",
         intro="The alert you trigger in Lab 26, as the JSON event your SIEM ingests.",
         code=[
             "$ cat eve.json | jq 'select(.event_type==\"alert\")'",
             "{",
             "  \"timestamp\": \"2026-08-19T10:42:07+0800\",",
             "  \"event_type\": \"alert\",",
             "  \"src_ip\": \"203.0.113.99\",",
             "  \"dest_ip\": \"10.0.0.5\",",
             "  \"alert\": {",
             "    \"signature\": \"GPL ATTACK_RESPONSE",
             "        id check returned root\",",
             "    \"category\": \"Potentially Bad Traffic\",",
             "    \"severity\": 2",
             "  }",
             "}",
         ],
         explain=[
             ("event_type", "One JSON object per event - jq filters alerts out of the flow, DNS and TLS records."),
             ("signature", "The ET rule that fired: the HTTP response contained uid=0(root) - a compromise tell."),
             ("src / dest", "Who attacked whom - the fields a SIEM correlates across all your sensors."),
         ]),

    dict(type="lab", num=26),

    # ================================================================
    # ACLs and content filtering  -> LAB 27
    # ================================================================
    dict(type="tiles", title="Access Control Lists (ACLs)",
         kicker="OBJ 4.3 · ACL", cols=2, accent="blue",
         items=[
             ("Top-down evaluation", "Rules are checked in order; the FIRST match wins and processing stops."),
             ("Implicit deny", "Whatever no rule matches is dropped - place your permits above the deny."),
             ("Match criteria", "Source and destination IP, protocol, port - the classic 5-tuple."),
             ("Where ACLs live", "Router interfaces, switch VLANs, cloud security groups, iptables chains."),
         ]),

    dict(type="worked", title="An iptables ACL, Line by Line",
         kicker="OBJ 4.3 · ACL IN PRACTICE",
         intro="The Lab 27 rule set: permit MySQL from one subnet, drop the rest.",
         code=[
             "$ iptables -I INPUT -p tcp --dport 3306 \\",
             "    -s 10.0.0.0/24 -j ACCEPT",
             "$ iptables -A INPUT -p tcp --dport 3306 -j DROP",
             "$ iptables -L INPUT -n -v --line-numbers",
             "",
             "num  target  prot  source        dpt",
             "1    ACCEPT  tcp   10.0.0.0/24   3306",
             "2    DROP    tcp   0.0.0.0/0     3306",
         ],
         explain=[
             ("-I vs -A", "-I inserts at the top, -A appends at the bottom - placement decides what matches first."),
             ("First match wins", "10.0.0.0/24 hits rule 1 and is accepted; everyone else falls through to the DROP."),
             ("Scope", "Only port 3306 is filtered here - pair with a default-deny policy for real hardening."),
         ]),

    dict(type="tiles", title="URL and Content Filtering",
         kicker="OBJ 4.3 · CONTENT FILTERING", cols=2, accent="teal",
         items=[
             ("URL filtering", "Allow or block by domain and category - malware, phishing, gambling lists."),
             ("Content filtering", "Inspect payloads - DLP stops card numbers leaving; AV strips attachments."),
             ("DNS filtering", "The cheapest control: a resolver that refuses to resolve known-bad domains."),
             ("TLS inspection", "Filtering encrypted traffic needs a re-signing proxy - governance required."),
         ]),

    dict(type="lab", num=27),

    # ================================================================
    # Physical security, lifecycle, recap  (OBJ 4.1)
    # ================================================================
    dict(type="tiles", title="Physical Security",
         kicker="OBJ 4.1 · PHYSICAL SECURITY", cols=2, accent="grey",
         items=[
             ("Cameras (CCTV)", "Detective control - record and deter; cover entrances, corridors and racks."),
             ("Locks", "Preventive - server rooms, racks and cages; smart locks log every entry."),
             ("Badge readers", "Authenticate entry per person and leave an audit trail."),
             ("Access control vestibule", "A two-door airlock defeats tailgating - one person per badge."),
             ("Security guards", "Flexible deterrent and response - verify visitors and deliveries."),
             ("Environmental sensors", "Door-open, temperature and humidity alarms in the data centre."),
         ]),

    dict(type="cards", title="Physical Control Categories",
         kicker="OBJ 4.1 · PHYSICAL SECURITY",
         cards=[
             ("blue", "Preventive", [
                 "Stop the event: locks, MFA, firewalls",
                 "Access control vestibules",
                 "Strongest when layered together"]),
             ("teal", "Detective", [
                 "Discover the event: CCTV, IDS, logs",
                 "Audits and SIEM alerting",
                 "Enables fast, informed response"]),
             ("violet", "Deterrent / compensating", [
                 "Warning signs, visible cameras",
                 "Guards deter casual attempts",
                 "Compensating controls cover gaps"]),
         ]),

    dict(type="tiles", title="System Life Cycle and Secure Disposal",
         kicker="OBJ 4.1 · ASSET LIFECYCLE", cols=2, accent="grey",
         items=[
             ("Asset tags and inventory", "You cannot secure what you do not track - tag and record every device."),
             ("Secure wipe", "DoD 5220.22-M-style overwrite or crypto-erase before any disposal."),
             ("Factory reset", "Acceptable only for devices that never held sensitive data."),
             ("Chain of custody", "A documented audit trail from decommission to certified destruction."),
         ]),

    dict(type="bullets", title="Exam Checkpoint - Numbers to Memorise",
         kicker="DOMAIN 4 · EXAM CHECKPOINT", size=18,
         items=[
             "RADIUS: UDP 1812/1813 (legacy 1645/1646) - TACACS+: TCP 49",
             "LDAP 389, LDAPS 636, Kerberos 88, HTTPS 443, SSH 22",
             "IDS detects on a mirror copy; IPS sits inline and blocks",
             "Screened subnet (DMZ) hosts public services between two firewalls",
             "MFA needs two DIFFERENT factors: know / have / are",
         ]),

    dict(type="big",
         line1="Layers, least privilege, verify everything.",
         line2="Domain 4 in one line: encrypt in transit and at rest, authenticate with multiple factors, segment aggressively, harden every device, and watch the logs.",
         kicker="DOMAIN 4 · RECAP", color="blue"),
]
