# -*- coding: utf-8 -*-
""" 
A simple implementation of Blockchain in Python. 

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
@reference: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
"""

import hashlib
import json

from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request

class Blockchain(object):
    """ A Blockchain object with a list of transactions and blocks. """
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create a genesis block.
        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self, proof, previous_hash):
        """ 
        Creates a new Block and adds it to the chain.
        
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New Block
        """
        block = {
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

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
            - Find a number p' such that the hash(pp') contains leading 4 zeroes, where p is the previous p'
            - p is the previous proof, and p' is the new proof

        
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False otherwise
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

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

# Instantiate our Node.
app = Flask(__name__)

# Generate a globally unique address for this node.
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must recieve a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message' : 'New block forged',
        'index'   : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400

    # Create new transaction
    index = blockchain.new_transaction(**values)

    response = {
        'message' : f'Transaction will be added to Block {index}',
    }
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain'  : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)