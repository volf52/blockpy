# -*- coding: utf-8 -*-
""" A simple implementation of Blockchain in Python. """

class Blockchain(object):
    """ A Blockchain object with a list of transactions and blocks. """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self):
        """ Creates a new Block and adds it to the chain. """
        pass
    
    def new_transaction(self):
        """ Adds a new transaction to the list of transactions. """
        pass
    
    @staticmethod
    def hash(block):
        """ Hash the block. """
        pass
    
    @property
    def last_block(self):
        """ Returns the last Block in the chain. """
        pass
    

