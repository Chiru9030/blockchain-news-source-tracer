import os
import hashlib
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class BlockchainManager:
    def __init__(self):
        self.rpc_url = os.getenv("POLYGON_RPC_URL")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        
        if self.rpc_url:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        else:
            self.w3 = None

    def record_verification(self, article_url, credibility_score):
        """
        Records the verification result on the blockchain.
        Returns the transaction hash.
        """
        # Create a unique hash for the record
        record_data = f"{article_url}-{credibility_score}-{time.time()}"
        record_hash = hashlib.sha256(record_data.encode()).hexdigest()
        
        if self.w3 and self.w3.is_connected() and self.private_key:
            # Real transaction logic would go here
            # For this MVP, we might just store the hash in a simple contract 
            # or send a 0-value tx with data.
            print("Connected to Blockchain. Preparing transaction...")
            try:
                # This is a placeholder for actual smart contract interaction
                # In a real app, we would build a transaction, sign it, and send it.
                # tx = self.contract.functions.record(article_url, score).build_transaction(...)
                # signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
                # tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                # return self.w3.to_hex(tx_hash)
                 return f"0x{record_hash} (Simulated Request on Real Connection)"
            except Exception as e:
                print(f"Blockchain Error: {e}")
                return self._mock_transaction(record_hash)
        else:
            if not self.w3:
                print("Warning: No Blockchain connection (RPC URL missing). Using simulation.")
            elif not self.private_key:
                 print("Warning: No Private Key provided. Read-only mode. Using simulation.")
            
            return self._mock_transaction(record_hash)

    def _mock_transaction(self, record_hash):
        # Simulate a transaction hash (Polygon tx hashes look like 0x...)
        return f"0x{record_hash[:60]}... (SIMULATED)"
