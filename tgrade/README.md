# Tgrade mainnet validator's guide

![Tgrade Guide by AnyValid](https://i.imgur.com/gGvPN5q.png)
____
Update and install necessary packages:
```bash
sudo apt update && sudo apt upgrade --yes && \
sudo apt install git build-essential ufw curl jq snapd screen ncdu nano fuse ufw --yes && 
```
Install go:
```bash
sudo snap install go --classic && \
echo 'export GOPATH="$HOME/go"' >> ~/.profile && \
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile && \
echo 'export PATH="$GOBIN:$PATH"' >> ~/.profile && \
source ~/.profile && \
go version
```
Clone repository and compile last version of binary (you can find releases here: [click](https://github.com/confio/tgrade/tags)):
```bash
git clone https://github.com/confio/tgrade
cd tgrade
git checkout v$(curl -s https://tgrade-rpc.anyvalid.com/abci_info | jq -r .result[].version)
make install
```
Init your keys and download genesis file:
```bash
tgrade init <moniker> --chain-id tgrade-mainnet-1
tgrade keys add <moniker>
wget https://raw.githubusercontent.com/confio/tgrade-networks/main/mainnet-1/config/genesis.json -O /root/.tgrade/config/genesis.json
```
Set up gas_price / persistent_peers / pruning:
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
Set up Tgrade service
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
Enable Tgrade daemon:
```bash
sudo systemctl enable tgrade
sudo systemctl daemon-reload
```
____
## If you want to synchronize your node from the 0 block:
Start Tgrade service and watch logs:
```bash
sudo systemctl restart tgrade
sudo journalctl -u tgrade -f -o cat
```
____

## Or you can quickly synchronize your node through State Sync:
Stop existing service and reset database:
```bash
sudo systemctl stop tgrade
tgrade tendermint unsafe-reset-all
```
Fill variables with data for State Sync:
```bash
RPC="https://tgrade-rpc.anyvalid.com:443"
RECENT_HEIGHT=$(curl -s $RPC/block | jq -r .result.block.header.height)
TRUST_HEIGHT=$((RECENT_HEIGHT - 500))
TRUST_HASH=$(curl -s "$RPC/block?height=$TRUST_HEIGHT" | jq -r .result.block_id.hash)
PEER="763baaaee37c63de0a517b9f12f2c1f153db6fab@65.109.18.170:26656"
```
Add variable values to config.toml:
```bash
sed -i.bak -E "s|^(enable[[:space:]]+=[[:space:]]+).*$|\1true| ; \
s|^(rpc_servers[[:space:]]+=[[:space:]]+).*$|\1\"$RPC,$RPC\"| ; \
s|^(trust_height[[:space:]]+=[[:space:]]+).*$|\1$TRUST_HEIGHT| ; \
s|^(trust_hash[[:space:]]+=[[:space:]]+).*$|\1\"$TRUST_HASH\"|" $HOME/.tgrade/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEER\"/" $HOME/.tgrade/config/config.toml
```
Start service and open journal:
```bash
sudo systemctl restart tgrade
sudo journalctl -u tgrade -f -o cat
```
____
*Wait for sync...*
____
Create validator (Do not forget to specify amount (1tgd = 1000000utgd) / keyname / moniker):
```bash
tgrade tx poe create-validator \
  --amount 1000000utgd \
  --vesting-amount 0utgd \
  --from <keyname> \
  --pubkey $(sudo tgrade tendermint show-validator) \
  --chain-id tgrade-mainnet-1 \
  --moniker "<your-validator-name>" \
  --fees 200000utgd \
  --gas auto \
  --gas-adjustment 1.4
```
After creating your own validator you can delegate more liquid and/or vesting tokens to your valiator on [Tgrade dapp](https://dapp.tgrade.finance/validators) or via command:
```bash
tgrade tx poe self-delegate <liquid tokens amount>utgd <vesting tokens amount>utgd \
  --from <keyname> \
  --gas auto \
  --gas-adjustment 1.4 \
  --chain-id tgrade-mainnet-1 \
  --fees 200000utgd 
```
