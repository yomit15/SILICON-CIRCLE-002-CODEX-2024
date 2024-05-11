from hashlib import sha256
import datetime
import time
import random
import json
from sys import exit

candidates = []
voter_code = 0

class Voter():
    def __init__(self, name, unique_id, timestamp=datetime.datetime.now()):
        self.name = name
        self.id = unique_id
        self.timestamp = timestamp
        self.nonce = random.randint(0, 1000000)
        self.key = str(self.calculate_key())
        self.voter_code = str(unique_id)
    def calculate_key(self):
        checksum = str(self.timestamp) + str(self.id) + str(self.nonce) + self.name
        return str(sha256(checksum.encode("utf-8")).hexdigest())

class Vote():
    def __init__(self, voter_key, vote_name):
        self.voter_key = voter_key
        isValidCandidate = False
        for candidate in candidates:
            if vote_name.lower() == candidate.lower():
                self.vote_name = vote_name
                isValidCandidate = True
        if isValidCandidate == False:
            print("Error : Specify a valid candidate")
            exit(1)

class Block():
    def __init__(self, vote_name, previousHash='', timestamp=datetime.datetime.now()):
        self.timestamp = timestamp
        self.vote_name = vote_name
        self.previousHash = previousHash
        self.hash = ''
        self.nonce = 0

    def calculate_hash(self):
        checksum = str(self.timestamp) + str(self.vote_name) + self.previousHash + str(self.nonce)
        return str(sha256(checksum.encode("utf-8")).hexdigest())

    def validate_block(self, difficulty):
        start_string = ''
        for i in range(difficulty):
            start_string += '0'
        while self.hash[:difficulty] != start_string:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block Validated: " + self.hash)

class BlockChain():
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.unvalidated_blocks = []
        self.previouslyVoted = []
        self.vote_count = dict()
        self.candidatesInitialized = False

    def create_genesis_block(self):
        genesis = Block("Genesis", "0")
        genesis.hash = genesis.calculate_hash()
        return genesis

    def validate_unvalidated_blocks(self):
        for vote_name in self.unvalidated_blocks:
            vote_name.validate_block(self.difficulty)
            print("Block validated: " + vote_name.hash)
            self.chain.append(vote_name)

    def create_block(self, vote, voter_name, voter_key):
        if self.candidatesInitialized == False:
            self.candidatesInitialized = True
            for candidate in candidates:
                self.vote_count[candidate] = 0
        voter_identifier = voter_name + voter_key
        if voter_identifier in self.previouslyVoted:
            raise ValueError("Error: A voter can only vote once!")
        else:
            self.previouslyVoted.append(voter_identifier)
            self.vote_count[vote.vote_name] += 1 
            self.unvalidated_blocks.append(Block(vote.vote_name, previousHash=self.chain[-1].hash))

    def get_votes(self):
        print(self.vote_count)
        return self.vote_count

    def is_chain_valid(self):
        for i in range(1, len(self.chain), 1):
            c_block = self.chain[i]  
            p_block = self.chain[i - 1]

            if c_block.hash != c_block.calculate_hash():
                return False

            if c_block.previousHash != p_block.hash:
                return False

        return True
    
    def get_votes(self):
        vote_count_with_timestamp = {
            "timestamp": int(time.time()),
            "vote_count": self.vote_count
        }
        with open("vote_count.json", "w") as outfile:
            json.dump(vote_count_with_timestamp, outfile)
        return self.vote_count
