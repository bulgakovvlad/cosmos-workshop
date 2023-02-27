# 🌐 RPC Endpoint

### Seed Node - Tgrade's official seed node by AnyValid&#x20;

#### You can connect via following command

```bash
sed -E -i 's/seeds = \".*\"/seeds = \"8639bc931d5721a64afc1ea52ca63ae40161bd26@194.163.144.63:26656\"/' $HOME/.tgrade/config/config.toml
```

#### Or input manually in config.toml file

```bash
8639bc931d5721a64afc1ea52ca63ae40161bd26@194.163.144.63:26656
```

#### And then restart your service

```bash
sudo systemctl restart tgrade
sudo journalctl -u tgrade -f -o cat
```

### RPC - You can use our high-performance archive RPC (Port 443)

`https://tgrade-rpc.anyvalid.com:443`

{% embed url="https://tgrade-rpc.anyvalid.com" %}
