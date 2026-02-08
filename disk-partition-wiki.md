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


## Adding a new disk
```
[root@rocky-minimal ~]# lsblk | grep sdc
sdc                8:32   0   20G  0 disk
```

**Create a Filesystem**

```
# To format as XFS
mkfs.xfs /dev/sdc
```
**Create the Partition**

`echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdc`

**Format the new partition**

`mkfs.xfs /dev/sdc1`

**Create Folder and Mount**

```
mkdir -p /opt/docker/data
mount /dev/sdc1 /opt/docker/data
```

**Ensure it persists after Reboot**
- Find the UUID: `blkid /dev/sdc1`
- Edit the fstab file: `vi /etc/fstab`
- Add this line at the bottom (replace the UUID with your actual result): `UUID=e3c50db3-1d8c-4d63-bd17-1429e9c9b1ae /opt/docker/data xfs defaults 0 2` 
