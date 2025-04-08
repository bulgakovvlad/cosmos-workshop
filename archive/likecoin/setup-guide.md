---
description: Follow the guide to set up your LikeCoin Mainnet node
---

# ⚙️ Setup Guide

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

#### Step 3: Clone repo and compile binary (you can find releases here: [click](https://github.com/humansdotai/humans/releases))

```bash
git clone https://github.com/likecoin/likecoin-chain
cd likecoin-chain
git checkout v4.2.0
make install
```

#### Step 4: Init your keys and download genesis file

```bash
liked init <moniker>
liked keys add <keyname>
curl https://raw.githubusercontent.com/likecoin/mainnet/master/genesis.json > ~/.liked/config/genesis.json
```

#### Step 5: Set up minimum gas price

```bash
sed -i.bak -e "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"10000nanolike\"/;" ~/.liked/config/app.toml
```

#### Step 6: Set up pruning (optional)

```
pruning="custom"
pruning_keep_recent="100"
pruning_keep_every="0"
pruning_interval="10"
sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.liked/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.liked/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.liked/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.liked/config/app.toml
```

#### Step 7: Set up LikeCoin service

```bash
sudo tee /etc/systemd/system/liked.service > /dev/null <<EOF
[Unit]
Description=LikeCoin daemon
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/liked start
Restart=on-failure
RestartSec=3
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
EOF
```

#### Step 7: Enable LikeCoin daemon

```bash
sudo systemctl enable liked
sudo systemctl daemon-reload
```

### If you want to synchronize your node from the 0 block:

#### Start LikeCoin service and check logs

```bash
sudo systemctl restart liked
sudo journalctl -u liked -f -o cat
```

Or you can quickly synchronize your node through State Sync:

{% content-ref url="state-sync-guide.md" %}
[state-sync-guide.md](state-sync-guide.md)
{% endcontent-ref %}
