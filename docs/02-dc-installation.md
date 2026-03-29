# Domain Controller Installation

## VM Configuration
- OS: Windows Server 2022 Standard Evaluation (Desktop Experience) 
    https://info.microsoft.com/ww-landing-windows-server-2022.html
- RAM 6144 MB
- CPUs: 4
- Disk: 60 GB
- Network Adapters:
    - Adapter 1: NAT(internet access, DHCP from VirtualBox)
    - Adapter 2: Internal Network (AD Traffic)

## Network Configuration
- INTERNAL adapter static IP: 172.16.0.1
- Subnet: 255.255.255.0
- Gateway: empty
- DNS: 127.0.0.1
- INTERNET adapter: DHCP (receives 10.0.2.x from VirtualBox NAT)

## Roles Installed
- Active Directory Domain Services (AD DS)
- DHCP Server
- DNS
- Remote Access (RAS/NAT)
- IIS

## Domain
- Forest: nfllab.local
- Domain Controller: WIN-UUI5LECBC03 (default, forgot to change before promoting to DC)

## Admin Accounts
- Built-in Administrator (initial setup only)
- a-pastidias (personal domain admin account)