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
```
```bash
git clone https://github.com/confio/tgrade
cd tgrade
git checkout <last version>
make install
```
```bash
tgrade init <moniker> --chain-id tgrade-mainnet-1
tgrade keys add <moniker> --recover
wget https://raw.githubusercontent.com/confio/tgrade-networks/main/mainnet-1/config/genesis.json -O /root/.tgrade/config/genesis.json
```
Setting up gas_price / persistent_peers / pruning:
```bash
sed -i "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"0.05utgd\"/;" $HOME/.tgrade/config/app.toml
sed -E -i 's/persistent_peers = \".*\"/persistent_peers = \"0a63421f67d02e7fb823ea6d6ceb8acf758df24d@142.132.226.137:26656,4a319eead699418e974e8eed47c2de6332c3f825@167.235.255.9:26656,6918efd409684d64694cac485dbcc27dfeea4f38@49.12.240.203:26656\"/' $HOME/.tgrade/config/config.toml
pruning="custom"
pruning_keep_recent="100"
pruning_keep_every="0"
pruning_interval="10"
sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.tgrade/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.tgrade/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.tgrade/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.tgrade/config/app.toml
```
```bash
sudo tee <<EOF >/dev/null /etc/systemd/system/tgrade.service
[Unit]
Description=Tgrade daemon
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/tgrade start
Restart=on-failure
RestartSec=3
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
EOF
```
