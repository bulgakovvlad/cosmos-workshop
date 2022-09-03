# Tgrade mainnet validator's guide

```bash
sudo apt update && sudo apt upgrade --yes && \
sudo apt install git build-essential ufw curl jq snapd screen ncdu nano fuse ufw --yes && 
```
```bash
sudo snap install go --classic && \
echo 'export GOPATH="$HOME/go"' >> ~/.profile && \
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile && \
echo 'export PATH="$GOBIN:$PATH"' >> ~/.profile && \
source ~/.profile && \
go version
````
