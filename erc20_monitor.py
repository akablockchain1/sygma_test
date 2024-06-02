import time
import requests
from web3 import Web3
from prometheus_client import start_http_server, Gauge

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider('YOUR_INFURA_OR_ALCHEMY_HTTP_PROVIDER'))

ERC20_CONTRACT_ADDRESS = '0xYourContractAddress'
ERC20_ABI = 'YourContractABI'

contract = web3.eth.contract(address=ERC20_CONTRACT_ADDRESS, abi=ERC20_ABI)

# Define Prometheus metrics
tx_failures_gauge = Gauge('erc20_tx_failures', 'Number of transaction failures')
gas_usage_gauge = Gauge('erc20_gas_usage', 'Gas usage of transactions')
contract_interactions_gauge = Gauge('erc20_contract_interactions', 'Number of contract interactions')

def monitor_erc20():
    # Example block range to monitor
    start_block = web3.eth.block_number - 1000
    end_block = web3.eth.block_number

    tx_failures = 0
    total_gas_used = 0
    contract_interactions = 0

    for block_number in range(start_block, end_block + 1):
        block = web3.eth.getBlock(block_number, full_transactions=True)
        for tx in block.transactions:
            if tx.to == ERC20_CONTRACT_ADDRESS:
                contract_interactions += 1
                try:
                    receipt = web3.eth.getTransactionReceipt(tx.hash)
                    total_gas_used += receipt.gasUsed
                    if receipt.status == 0:
                        tx_failures += 1
                except:
                    tx_failures += 1

    tx_failures_gauge.set(tx_failures)
    gas_usage_gauge.set(total_gas_used)
    contract_interactions_gauge.set(contract_interactions)

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8000)

    # Monitor the contract in a loop
    while True:
        monitor_erc20()
        time.sleep(60)  # Adjust the sleep time as needed
