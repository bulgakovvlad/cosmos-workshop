# 🔌 State Sync Guide

<details>

<summary>Step 1: Stop existing service and reset database</summary>

```bash
sudo systemctl stop firmachaind
firmachaind unsafe-reset-all --keep-addr-book
```

</details>

<details>

<summary>Step 2: Fill variables with data for State Sync</summary>

```bash
RPC="https://firmachain-rpc.anyvalid.com:443"
RECENT_HEIGHT=$(curl -s $RPC/block | jq -r .result.block.header.height)
TRUST_HEIGHT=$((RECENT_HEIGHT - 1000))
TRUST_HASH=$(curl -s "$RPC/block?height=$TRUST_HEIGHT" | jq -r .result.block_id.hash)
PEER="c73d22b6a749534ff17c3ccebb00bb2b2215c525@207.180.239.3:26656"
```

</details>

<details>

<summary>Step 3: Add variable values to config.toml</summary>

```bash
sed -i.bak -E "s|^(enable[[:space:]]+=[[:space:]]+).*$|\1true| ; \
s|^(rpc_servers[[:space:]]+=[[:space:]]+).*$|\1\"$RPC,$RPC\"| ; \
s|^(trust_height[[:space:]]+=[[:space:]]+).*$|\1$TRUST_HEIGHT| ; \
s|^(trust_hash[[:space:]]+=[[:space:]]+).*$|\1\"$TRUST_HASH\"|" $HOME/.firmachain/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEER\"/" $HOME/.firmachain/config/config.toml
```

</details>

<details>

<summary>Step 4: Start service and open journal</summary>

```bash
sudo systemctl restart firmachaind
sudo journalctl -u firmachaind -f -o cat
```

</details>
