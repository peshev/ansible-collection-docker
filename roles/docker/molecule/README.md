```shell
docker rm $(docker ps -a | grep download-531ded | cut -d\  -f1)
rm molecule/shared/offline_assets/ -rf
molecule --base-config molecule/shared/base.yml destroy -s offline-prepare-install
```