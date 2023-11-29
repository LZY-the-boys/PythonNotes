sudo umount /dev/nvme0n1
sudo umount /dev/nvme0n2
sudo umount /dev/nvme0n3
sudo umount /dev/nvme0n4
sudo umount /dev/nvme0n5
sudo umount /dev/nvme0n6
sudo umount /dev/nvme0n7
sudo umount /dev/nvme0n8
sudo vgcreate mydata /dev/nvme0n1 /dev/nvme0n2 /dev/nvme0n3 /dev/nvme0n4 /dev/nvme0n5 /dev/nvme0n6 /dev/nvme0n7 /dev/nvme0n8
sudo lvcreate -l 100%FREE --type raid0 -n mylogicdata mydata
sudo mkfs.ext4 /dev/mydata/mylogicdata
sudo mount /dev/mapper/mydata-mylogicdata /data