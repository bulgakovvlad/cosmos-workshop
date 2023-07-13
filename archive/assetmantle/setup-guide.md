---
description: Follow the guide to set up your AssetMantle Mainnet node
---

# ⚙ Setup Guide

#### Step 1: Update and install necessary packages

```bash
sudo apt update && sudo apt upgrade --yes && \
sudo apt install git build-essential ufw curl jq snapd screen ncdu nano fuse ufw --yes
```

#### Step 2: Install Go

```bash
sudo snap install go --classic && \
echo 'export GOPATH="$HOME/go"' >> ~/.profile && \
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile && \
echo 'export PATH="$GOBIN:$PATH"' >> ~/.profile && \
source ~/.profile && \
go version
```

#### Step 3: Clone the repository and compile binary

```bash
git clone https://github.com/AssetMantle/node.git
cd node
git checkout tags/v0.3.0
make install
```

#### Step 4: Init your keys and download genesis file

```bash
mantleNode init <moniker> --chain-id mantle-1
mantleNode keys add <keyname>
curl https://raw.githubusercontent.com/AssetMantle/genesisTransactions/main/mantle-1/final_genesis.json > $HOME/.mantleNode/config/genesis.json
```

#### Step 5: Set up AssetMantle system service

```bash
sudo tee /etc/systemd/system/assetmantle.service > /dev/null <<EOF
[Unit]
Description=AssetMantleNode Service
Requires=network-online.target
After=network-online.target

[Service]
User=root
Restart=on-failure
RestartSec=3
MemoryDenyWriteExecute=yes
LimitNOFILE=65535
ExecStart=/root/go/bin/mantleNode start --x-crisis-skip-assert-invariants

[Install]
WantedBy=multi-user.target
EOF
```

#### Step 6: Enable AssetMantle daemon

```bash
sudo systemctl daemon-reload
sudo systemctl enable assetmantle
```

### If you want to synchronize your node from the 0 block:

#### Start AssetMantle service and watch logs

```bash
sudo systemctl start assetmantle
journalctl -u assetmantle -f -o cat
```

Or you can quickly synchronize your node through State Sync:

{% content-ref url="state-sync-guide.md" %}
[state-sync-guide.md](state-sync-guide.md)
{% endcontent-ref %}
