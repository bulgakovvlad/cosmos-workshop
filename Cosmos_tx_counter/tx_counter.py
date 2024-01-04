from datetime import datetime
import requests
from tqdm import tqdm

def get_block_heights(rpc_address):
    """
    Retrieves the earliest and latest block heights from the given RPC server.
    """
    try:
        response = requests.get(f"{rpc_address}/status")
        data = response.json()
        earliest_block_height = data['result']['sync_info']['earliest_block_height']
        latest_block_height = data['result']['sync_info']['latest_block_height']
        return earliest_block_height, latest_block_height
    except Exception as e:
        print(f"Error fetching block heights: {e}")
        return None, None

def count_transactions(rpc_address, start_block, end_block):
    transaction_count = {}
    total_transactions = 0

    for block in tqdm(range(start_block, end_block + 1), desc="Processing blocks"):
        try:
            response = requests.get(f"{rpc_address}/block_results?height={block}")
            block_data = response.json()
            
            txs_results = block_data.get('result', {}).get('txs_results', [])
            if txs_results is None:
                txs_results = []

            transactions_in_block = sum(1 if 'code' in tx and tx['code'] == 0 else 0 for tx in txs_results)

            transaction_count[block] = transactions_in_block
            total_transactions += transactions_in_block
        except Exception as e:
            print(f"Error fetching block {block}: {e}")

    return transaction_count, total_transactions


def main():
    rpc_address = input("Enter the RPC server address (default http://localhost:26657): ")
    rpc_address = rpc_address.strip() or "http://localhost:26657"

    earliest_block_height, latest_block_height = get_block_heights(rpc_address)
    if earliest_block_height is None or latest_block_height is None:
        return

    start_block_input = input(f"Enter the start block number (default {earliest_block_height}): ")
    start_block = int(start_block_input) if start_block_input.strip() else int(earliest_block_height)

    end_block_input = input(f"Enter the end block number (default {latest_block_height}): ")
    end_block = int(end_block_input) if end_block_input.strip() else int(latest_block_height)

    transaction_count, total_transactions = count_transactions(rpc_address, start_block, end_block)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"block_transaction_report_{timestamp}.txt"
    
    with open(filename, "w") as file:
        file.write(f"Total transactions in blocks from {start_block} to {end_block}: {total_transactions}\n")
        file.write("Details per block:\n")
        for block, count in transaction_count.items():
            file.write(f"{block}: {count} transactions\n")

    print(f"Report generated in '{filename}'.")

if __name__ == "__main__":
    main()
