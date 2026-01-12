# Remote Access Guide - Laptop to Desktop

This guide shows you how to access your AI Coding Assistant running on your desktop from your laptop remotely.

---

## Overview

```
Laptop (Client) -----> Network -----> Desktop (Server)
                          |
                    [SSH/VPN/Tunnel]
                          |
                   AI Assistant Services
```

---

## Option 1: SSH Tunnel (Recommended for Technical Users)

### Advantages
- ✅ Secure (encrypted)
- ✅ No third-party services
- ✅ Free
- ✅ Works on any network

### Prerequisites
- SSH access to desktop
- OpenSSH installed on both machines

### Setup on Desktop (Server)

#### Windows Desktop

1. **Install OpenSSH Server**
```powershell
# Run as Administrator
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start SSH service
Start-Service sshd

# Set to start automatically
Set-Service -Name sshd -StartupType 'Automatic'

# Configure firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

2. **Get Desktop IP Address**
```powershell
# Get local IP
ipconfig | findstr IPv4
```

Note your IP (e.g., `192.168.1.100`)

#### Linux/Mac Desktop

SSH is usually pre-installed. Start it:
```bash
# Linux
sudo systemctl start sshd
sudo systemctl enable sshd

# Mac
sudo systemsetup -setremotelogin on

# Get IP
ip addr show  # Linux
ifconfig      # Mac
```

### Access from Laptop

#### Method 1: Port Forwarding (Single Service)

```bash
# Forward backend API (port 8000)
ssh -L 8000:localhost:8000 username@desktop-ip

# Forward frontend (port 3000)
ssh -L 3000:localhost:3000 username@desktop-ip

# Forward multiple ports
ssh -L 8000:localhost:8000 \
    -L 3000:localhost:3000 \
    -L 9001:localhost:9001 \
    username@desktop-ip
```

Now access on laptop:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- MinIO: http://localhost:9001

#### Method 2: SOCKS Proxy (All Services)

```bash
# Create SOCKS proxy
ssh -D 8080 -N username@desktop-ip

# Configure browser to use SOCKS proxy:
# Settings → Network → Manual Proxy
# SOCKS Host: localhost
# Port: 8080
```

#### Method 3: SSH Config for Easy Connection

Create `~/.ssh/config` on laptop:

```
Host ai-desktop
    HostName 192.168.1.100  # Your desktop IP
    User your-username
    LocalForward 3000 localhost:3000
    LocalForward 8000 localhost:8000
    LocalForward 9001 localhost:9001
    LocalForward 6333 localhost:6333
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Then simply:
```bash
ssh ai-desktop
```

### Keep SSH Tunnel Running in Background

#### Using tmux (Recommended)
```bash
# On laptop
ssh username@desktop-ip

# Once connected
tmux new -s tunnel
# Press Ctrl+B then D to detach

# Reconnect anytime
ssh username@desktop-ip -t tmux attach -t tunnel
```

#### Using autossh (Auto-reconnect)
```bash
# Install autossh
# Mac: brew install autossh
# Linux: sudo apt install autossh

# Run with auto-reconnect
autossh -M 0 -f -N -L 3000:localhost:3000 -L 8000:localhost:8000 username@desktop-ip
```

---

## Option 2: Tailscale (Recommended for Ease of Use)

### Advantages
- ✅ Easiest setup
- ✅ Works across any network (even with NAT)
- ✅ Encrypted mesh VPN
- ✅ Free for personal use (up to 100 devices)
- ✅ Mobile apps available

### Setup

1. **Install on Desktop**
   - Download: https://tailscale.com/download
   - Install and sign in

2. **Install on Laptop**
   - Download and install
   - Sign in with same account

3. **Get Tailscale IP**
   ```bash
   # On desktop
   tailscale ip -4
   ```
   Example output: `100.64.0.2`

4. **Access from Laptop**
   ```
   Frontend: http://100.64.0.2:3000
   Backend:  http://100.64.0.2:8000
   ```

### Enable MagicDNS (Optional)

Tailscale Admin Console → DNS → Enable MagicDNS

Then access by hostname:
```
http://desktop:3000
http://desktop:8000
```

---

## Option 3: Ngrok (Public URL, Great for Demos)

### Advantages
- ✅ Public URL for sharing
- ✅ Works from anywhere
- ✅ HTTPS support
- ⚠️ Requires account
- ⚠️ Free tier has limitations

### Setup

1. **Install Ngrok on Desktop**
   - Download: https://ngrok.com/download
   - Sign up for free account
   - Get auth token

2. **Authenticate**
   ```bash
   ngrok authtoken YOUR_TOKEN
   ```

3. **Expose Services**
   ```bash
   # Expose frontend
   ngrok http 3000

   # Or use ngrok config for multiple services
   ```

4. **Create ngrok.yml**
   ```yaml
   version: "2"
   authtoken: YOUR_TOKEN
   tunnels:
     frontend:
       proto: http
       addr: 3000
     backend:
       proto: http
       addr: 8000
   ```

5. **Start All Tunnels**
   ```bash
   ngrok start --all
   ```

You'll get public URLs like:
```
https://abc123.ngrok.io -> localhost:3000
https://def456.ngrok.io -> localhost:8000
```

---

## Option 4: WireGuard VPN (Advanced)

### Advantages
- ✅ Fast and secure
- ✅ Full network access
- ✅ Modern protocol
- ⚠️ Requires configuration

### Setup on Desktop (Server)

1. **Install WireGuard**
   ```bash
   # Linux
   sudo apt install wireguard

   # Windows
   # Download from: https://www.wireguard.com/install/
   ```

2. **Generate Keys**
   ```bash
   wg genkey | tee privatekey | wg pubkey > publickey
   ```

3. **Configure Server** (`/etc/wireguard/wg0.conf`)
   ```ini
   [Interface]
   Address = 10.0.0.1/24
   PrivateKey = <server-private-key>
   ListenPort = 51820

   [Peer]
   PublicKey = <laptop-public-key>
   AllowedIPs = 10.0.0.2/32
   ```

4. **Start WireGuard**
   ```bash
   sudo wg-quick up wg0
   sudo systemctl enable wg-quick@wg0
   ```

### Setup on Laptop (Client)

1. **Install WireGuard**

2. **Configure Client** (`wg0.conf`)
   ```ini
   [Interface]
   Address = 10.0.0.2/24
   PrivateKey = <laptop-private-key>

   [Peer]
   PublicKey = <server-public-key>
   Endpoint = desktop-public-ip:51820
   AllowedIPs = 10.0.0.0/24
   PersistentKeepalive = 25
   ```

3. **Connect**
   ```bash
   sudo wg-quick up wg0
   ```

4. **Access Services**
   ```
   http://10.0.0.1:3000
   http://10.0.0.1:8000
   ```

---

## Option 5: CloudFlare Tunnel (Zero Trust)

### Advantages
- ✅ No open ports needed
- ✅ Free tier available
- ✅ DDoS protection
- ✅ Access control

### Setup

1. **Install cloudflared on Desktop**
   ```bash
   # Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Authenticate**
   ```bash
   cloudflared tunnel login
   ```

3. **Create Tunnel**
   ```bash
   cloudflared tunnel create ai-assistant
   ```

4. **Configure Tunnel** (`~/.cloudflared/config.yml`)
   ```yaml
   tunnel: <tunnel-id>
   credentials-file: /path/to/credentials.json

   ingress:
     - hostname: ai-assistant.yourdomain.com
       service: http://localhost:3000
     - hostname: api.ai-assistant.yourdomain.com
       service: http://localhost:8000
     - service: http_status:404
   ```

5. **Run Tunnel**
   ```bash
   cloudflared tunnel run ai-assistant
   ```

6. **Access from Laptop**
   ```
   https://ai-assistant.yourdomain.com
   https://api.ai-assistant.yourdomain.com
   ```

---

## Comparison Table

| Solution | Ease of Use | Security | Cost | Network Requirements | Best For |
|----------|-------------|----------|------|---------------------|----------|
| **SSH Tunnel** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | SSH access | Technical users |
| **Tailscale** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free* | Internet | Everyone |
| **Ngrok** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Free/Paid | Internet | Demos, testing |
| **WireGuard** | ⭐⭐ | ⭐⭐⭐⭐⭐ | Free | Open port 51820 | Advanced users |
| **CloudFlare** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Free/Paid | Internet | Production |

---

## Recommended Setup

### For Home Network (Same WiFi)
```bash
# Just use local IP directly
# Desktop IP: 192.168.1.100
# Access: http://192.168.1.100:3000
```

### For Remote Access (Different Networks)
**Best option: Tailscale**
1. Install Tailscale on both machines
2. Access via Tailscale IP or hostname
3. Works everywhere, always secure

### For Public Demo/Sharing
**Best option: Ngrok**
1. Run ngrok on desktop
2. Share public URL
3. Revoke when done

---

## Security Best Practices

1. **Never expose services directly to internet**
   ```bash
   # DON'T DO THIS
   docker-compose.yml:
     ports:
       - "0.0.0.0:8000:8000"  # ❌ Exposes to world
   ```

2. **Use strong SSH keys**
   ```bash
   # Generate strong key
   ssh-keygen -t ed25519 -C "your-email@example.com"

   # Copy to desktop
   ssh-copy-id username@desktop-ip
   ```

3. **Enable firewall**
   ```bash
   # Windows
   netsh advfirewall set allprofiles state on

   # Linux
   sudo ufw enable
   sudo ufw allow 22/tcp  # SSH only
   ```

4. **Use VPN for sensitive data**
   - Tailscale or WireGuard recommended
   - Don't use public tunnels for production

---

## Troubleshooting

### SSH Connection Refused
```bash
# Check SSH service
# Windows
Get-Service sshd

# Linux
sudo systemctl status sshd

# Check firewall
# Windows
netsh advfirewall firewall show rule name=sshd

# Linux
sudo ufw status
```

### Can't Access Desktop from Outside Network
```bash
# Check if desktop has public IP
curl ifconfig.me  # On desktop

# If behind router, you need:
# 1. Port forwarding on router, OR
# 2. Use Tailscale/Ngrok
```

### Tailscale Not Working
```bash
# Check status
tailscale status

# Restart
sudo tailscale down
sudo tailscale up

# Check firewall allows Tailscale
```

---

## Performance Tips

1. **Use compression for slow connections**
   ```bash
   ssh -C username@desktop-ip
   ```

2. **Reduce latency with connection reuse**
   ```
   # In ~/.ssh/config
   Host *
       ControlMaster auto
       ControlPath ~/.ssh/sockets/%r@%h-%p
       ControlPersist 600
   ```

3. **Optimize Docker for remote access**
   ```yaml
   # docker-compose.yml
   services:
     backend:
       environment:
         - TIMEOUT=300  # Increase timeouts
   ```

---

## Scripts

### Auto-Connect Script (laptop-connect.sh)

```bash
#!/bin/bash

DESKTOP_IP="192.168.1.100"  # Change this
USERNAME="your-username"     # Change this

echo "Connecting to AI Assistant on desktop..."

# Create SSH tunnel with port forwarding
ssh -N -f \
  -L 3000:localhost:3000 \
  -L 8000:localhost:8000 \
  -L 9001:localhost:9001 \
  $USERNAME@$DESKTOP_IP

echo "Connected! Access at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  MinIO:    http://localhost:9001"
echo ""
echo "To disconnect: pkill -f 'ssh -N -f'"
```

Usage:
```bash
chmod +x laptop-connect.sh
./laptop-connect.sh
```

---

## Next Steps

1. ✅ Remote access configured
2. 🏥 **Fine-tune for NHS data** → See `NHS_FINETUNING.md`
3. 🔐 **Add authentication** → Secure your deployment
4. 📊 **Set up monitoring** → Track usage and performance
