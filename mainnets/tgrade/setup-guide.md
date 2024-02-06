---
description: Follow the guide to set up your Dymension Mainnet node
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
git clone https://github.com/dymensionxyz/dymension
cd dymension
git checkout v$(curl -s https://dymension-rpc.anyvalid.com/abci_info | jq -r .result[].version)
make install
```

#### Step 4: Init your keys and download genesis file

```bash
dymd init <moniker> --chain-id dymension_1100-1
dymd keys add <keyname>
wget https://github.com/dymensionxyz/networks/raw/main/mainnet/dymension/genesis.json -O /root/.dymension/config/genesis.json
```

#### Step 5: Set up gas\_price / persistent\_peers / pruning

```bash
sed -i "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"20000000000adym\"/;" $HOME/.dymension/config/app.toml
sed -E -i 's/persistent_peers = \".*\"/persistent_peers = \"5f9ed4b975e0896b8ea862d29a45658e38b4f95d@88.99.140.176:26606\"/' $HOME/.dymension/config/config.toml
pruning="custom"
pruning_keep_recent="100"
pruning_keep_every="0"
pruning_interval="10"
sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.dymension/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.dymension/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.dymension/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.dymension/config/app.toml
```

#### Step 6: Set up Dymension service

```bash
sudo tee /etc/systemd/system/dymd.service > /dev/null <<EOF
[Unit]
Description=Dymension daemon
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/dymd start
Restart=on-failure
RestartSec=3
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
EOF
```

#### Step 7: Enable Dymension daemon

```bash
sudo systemctl enable dymd
sudo systemctl daemon-reload
```

### If you want to synchronize your node from the 0 block:

#### Start Dymension service and watch logs

```bash
sudo systemctl restart dymd
sudo journalctl -u dymd -f -o cat
```

Or you can quickly synchronize your node through State Sync:

{% content-ref url="../tgrade-1/state-sync-guide.md" %}
[state-sync-guide.md](../tgrade-1/state-sync-guide.md)
{% endcontent-ref %}
