# 🔌 State Sync Guide

{% hint style="info" %}
State Sync allows to sync a node state by fetching a snapshot of the network state at a recent height, instead of fetching and replaying all historical blocks.
{% endhint %}

#### Step 1: Stop existing service and reset database

```bash
sudo systemctl stop tgrade
tgrade tendermint unsafe-reset-all --keep-addr-book
```

#### Step 2: Fill variables with data for State Sync

```bash
RPC="https://tgrade-rpc.anyvalid.com:26637"
RECENT_HEIGHT=$(curl -s $RPC/block | jq -r .result.block.header.height)
TRUST_HEIGHT=$((RECENT_HEIGHT - 1000))
TRUST_HASH=$(curl -s "$RPC/block?height=$TRUST_HEIGHT" | jq -r .result.block_id.hash)
PEER="f7dd1c57e6aecbe415af69613a6966b06f8b21c9@88.99.140.176:26636"
```

#### Step 3: Add variable values to config.toml

```bash
sed -i.bak -E "s|^(enable[[:space:]]+=[[:space:]]+).*$|\1true| ; \
s|^(rpc_servers[[:space:]]+=[[:space:]]+).*$|\1\"$RPC,$RPC\"| ; \
s|^(trust_height[[:space:]]+=[[:space:]]+).*$|\1$TRUST_HEIGHT| ; \
s|^(trust_hash[[:space:]]+=[[:space:]]+).*$|\1\"$TRUST_HASH\"|" $HOME/.tgrade/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEER\"/" $HOME/.tgrade/config/config.toml
```

#### Step 4: Start service and open journal

```bash
sudo systemctl restart tgrade
sudo journalctl -u tgrade -f -o cat
```
