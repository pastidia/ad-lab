# Oracle VirtualBox Setup

## My Envcironment
- OS: Fedora Workstation 43
- Hypervisor: VirtualBox

## Installation

Install dependencies:
```bash
sudo dnf install kernel-devel kernel-headers dkms
```

Install VirtualBox
```bash
sudo dnf install virtualbox
```

Loadthe VirtualBox kernel module:
```bash
sudo modprobe vboxdrv
```

Verify the module loaded successfully:
```bash
lsmod | grep vboxdrv
```

The output should be 'vboxdrv'.

Add your user to the vboxusers group:
```bash
sudo usermod -aG vboxusers $USER
```

Log out and back in, and verify the group was added
```bash
groups
```

It should output 'vboxusers'