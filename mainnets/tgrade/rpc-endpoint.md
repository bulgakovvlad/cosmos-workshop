# 🌐 RPC Endpoint

### Seed Node - Tgrade's official seed node by AnyValid&#x20;

<details>

<summary>You can connect via following command</summary>

```bash
sed -E -i 's/seeds = \".*\"/seeds = \"8639bc931d5721a64afc1ea52ca63ae40161bd26@194.163.144.63:26656\"/' $HOME/.tgrade/config/config.toml
```

</details>

<details>

<summary>Or input manually in config.toml file</summary>

```bash
8639bc931d5721a64afc1ea52ca63ae40161bd26@194.163.144.63:26656
```

</details>

<details>

<summary>And then restart your service</summary>

```bash
sudo systemctl restart tgrade
sudo journalctl -u tgrade -f -o cat
```

</details>

### RPC - You can use our high-performance archive RPC (Port 443)

`https://tgrade-rpc.anyvalid.com:443`

{% embed url="https://tgrade-rpc.anyvalid.com" %}
