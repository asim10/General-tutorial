### Document for disk partitioning commands

# Increase the size of a disk
```
[root@rocky-minimal adinda]# lsblk
NAME             MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda                8:0    0   20G  0 disk
└─sda1             8:1    0   10G  0 part /opt/homelab
```
Install the utility (if you don't have it):
- Ubuntu/Debian: `sudo apt install cloud-guest-utils`
- CentOS/RHEL: `sudo yum install cloud-utils-growpart`

**Run growpart:** Identify the disk and the partition number
`sudo growpart /dev/sda 1`

**Expand the Filesystem**
- For ext4 filesystems: `sudo resize2fs /dev/sda1`
- For XFS filesystems: `sudo xfs_growfs /opt/homelab`

**Verify the Changes**

Run your `lsblk` command again to see the new size:

you can also run `df -h /opt/homelab` to confirm the usable space in the OS.
