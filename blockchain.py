# -*- coding: utf-8 -*-
""" 
A simple implementation of Blockchain in Python. 

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
@reference: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
"""

import hashlib
import json
from time import time


class Blockchain(object):
    """ A Blockchain object with a list of transactions and blocks. """
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create a genesis block.
        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self):
        """ 
        Creates a new Block and adds it to the chain.
        
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New Block
        """
        block =
        {
            'index' : len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        # Reset the current list of transactions.
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """ 
        Adds a new transaction to the list of transactions. 
        
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    @staticmethod
    def hash(block):
        """ 
        Creates a SHA-256 hash of a block.

        :param block: <dict> Block
        :return: <str> The hash
        """

        # We must make sure the dictionary is ordered or we will have incosistent hashes.
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    
    @property
    def last_block(self):
        """ Returns the last Block in the chain. """
        return self.chain[-1]
    

