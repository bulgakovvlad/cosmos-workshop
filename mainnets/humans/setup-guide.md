---
description: Follow the guide to set up your Humans Mainnet node
---

# ⚙ Setup Guide

#### **Step 1: Update and install necessary packages**

```bash
sudo apt update && sudo apt upgrade --yes && \
sudo apt install git build-essential ufw curl jq snapd screen ncdu nano fuse ufw --yes
```

#### **Step 2: Install Go**

```bash
sudo snap install go --classic && \
echo 'export GOPATH="$HOME/go"' >> ~/.profile && \
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile && \
echo 'export PATH="$GOBIN:$PATH"' >> ~/.profile && \
source ~/.profile && \
go version
```

#### Step 3: Clone repo and compile binary (you can find releases here: [click](https://github.com/confio/tgrade/tags))

```bash
git clone https://github.com/humansdotai/humans
cd humans
git checkout v$(curl -s https://humans-rpc.anyvalid.com:26627/abci_info | jq -r .result[].version)
make install
```

#### Step 4: Init your keys and download genesis file

```bash
humansd init <moniker> --chain-id humans_1089-1
humansd keys add <keyname>
wget https://anyvalid.com/humans/genesis.json -O $HOME/.humansd/config/genesis.json
wget https://anyvalid.com/humans/addrbook.json -O $HOME/.humansd/config/addrbook.json
```

#### Step 5: Set up gas\_price / persistent\_peers / pruning

```bash
sed -i "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"0.1aheart\"/;" $HOME/.humansd/config/app.toml
sed -E -i 's/persistent_peers = \".*\"/persistent_peers = \"0a63421f67d02e7fb823ea6d6ceb8acf758df24d@142.132.226.137:26656,4a319eead699418e974e8eed47c2de6332c3f825@167.235.255.9:26656,6918efd409684d64694cac485dbcc27dfeea4f38@49.12.240.203:26656\"/' $HOME/.humansd/config/config.toml
pruning="custom"
pruning_keep_recent="100"
pruning_keep_every="0"
pruning_interval="10"
sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.humansd/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.humansd/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.humansd/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.humansd/config/app.toml
```

#### Step 6: Set up Humans service

```bash
sudo tee /etc/systemd/system/humansd.service > /dev/null <<EOF
[Unit]
Description=Humansd daemon
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/humansd start
Restart=on-failure
RestartSec=3
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
EOF
```

#### Step 7: Enable Humans daemon

```bash
sudo systemctl enable humansd
sudo systemctl daemon-reload
```

### If you want to synchronize your node from the 0 block:

#### Start Humans service and watch logs

```bash
sudo systemctl restart humansd
sudo journalctl -u humansd -f -o cat
```

Or you can quickly synchronize your node through State Sync:

{% content-ref url="state-sync-guide.md" %}
[state-sync-guide.md](state-sync-guide.md)
{% endcontent-ref %}
