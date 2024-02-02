# 🔌 State Sync Guide

{% hint style="info" %}
State Sync allows to sync a node state by fetching a snapshot of the network state at a recent height, instead of fetching and replaying all historical blocks.
{% endhint %}

#### Step 1: Stop existing service and reset database

```bash
sudo systemctl stop umeed
umeed tendermint unsafe-reset-all --keep-addr-book
```

#### Step 2: Fill variables with data for State Sync

```bash
RPC="https://umee-rpc.anyvalid.com:26647"
RECENT_HEIGHT=$(curl -s $RPC/block | jq -r .result.block.header.height)
TRUST_HEIGHT=$((RECENT_HEIGHT - 1000))
TRUST_HASH=$(curl -s "$RPC/block?height=$TRUST_HEIGHT" | jq -r .result.block_id.hash)
PEER="f827a823a54d1deb02324362c4b81f275e596621@88.99.140.176:26646"
```

#### Step 3: Add variable values to config.toml

```bash
sed -i.bak -E "s|^(enable[[:space:]]+=[[:space:]]+).*$|\1true| ; \
s|^(rpc_servers[[:space:]]+=[[:space:]]+).*$|\1\"$RPC,$RPC\"| ; \
s|^(trust_height[[:space:]]+=[[:space:]]+).*$|\1$TRUST_HEIGHT| ; \
s|^(trust_hash[[:space:]]+=[[:space:]]+).*$|\1\"$TRUST_HASH\"|" $HOME/.umee/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEER\"/" $HOME/.umee/config/config.toml
```

#### Step 4: Start service and open journal

```bash
sudo systemctl restart umeed
sudo journalctl -u umeed -f -o cat
```
