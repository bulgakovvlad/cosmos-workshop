# 🔌 Snapshot Guide

#### Step 1: Stop existing service and reset database

```bash
sudo systemctl stop nolusd
cp $HOME/.nolus/data/priv_validator_state.json $HOME/priv_validator_state.json
nolusd tendermint unsafe-reset-all --home $HOME/.nolus --keep-addr-book
```

#### Step 2: Download nolus data

```bash
wget http://nolus-rpc.anyvalid.com/nolus/data_nolus-rila.tar
tar -xf data_nolus-rila.tar -C $HOME/.nolus/data/
rm data_nolus-rila.tar
```

#### Step 3: Download nolus wasm directory

```bash
wget http://nolus-rpc.anyvalid.com/nolus/wasm_nolus-rila.tar
mkdir $HOME/.nolus/wasm/
tar -xf wasm_nolus-rila.tar -C $HOME/.nolus/wasm/
rm wasm_nolus-rila.tar
```

#### Step 4: Restore your `priv_validator_state.json` file

```bash
mv $HOME/priv_validator_state.json $HOME/.nolus/data/priv_validator_state.json
```

#### Step 5: Start service and open journal

```bash
sudo systemctl restart assetmantle
sudo journalctl -u assetmantle -f -o cat
```
