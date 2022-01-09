import hashlib
import base64
import json
from time import time
from . QrCodegenerator import generateqrcode
from io import BytesIO

class Singleton_base(object):
    chain = []
    pending_data ={"url":"EMPTYURL"}
    genenesisceted=False
    _instance = None
    def __new__(class_, *args, **kwargs):
        
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            
            
        return class_._instance

class Blockchain(Singleton_base):

    def __init__(self):
        
         # this is the block chain that we shall be adding to
        #self.pending_data = []
      
        if not ( self.genenesisceted):
            self.create_new_block(previous_hash="Genesis Block", proof=100)
            self.genenesisceted=True

# Create a new block listing key/value pairs of block information in a JSON object. 
# The dictionary will take the following key-value pairs:

# Index: An index key will store the blockchain’s length. It is represented by the chain variable in the __init__ method with an added value of one(1). We will use this variable to access each block in the chain.

# Timestamp: The timestamp key will take a value of the current Date and Time the block was created or mined.

# Proof: This key will receive a proof value that will be passed to the function when called. Note that this variable refers to the proof of work.

# Previous hash: Lastly, the previous hash key takes a value of previous_hash from the function which is equivalent to the hash of the previous block.

# Reset the list of pending transactions & append the newest block to the chain.
    def create_new_block(self, proof, previous_hash=None):
       
        image,qrfilename=generateqrcode(self.pending_data["url"])

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str2=str(img_str, encoding='utf-8')

       
        print(self.pending_data)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.pending_data,#Data to add to the chain 
            'data2':img_str2,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        } #new block created
        self.pending_data = ""
        self.chain.append(block) # new block appended

        return block,qrfilename # we returned the new block created

#Search the blockchain for the most recent block.

    @property
    def get_previous_block(self):

        return self.chain[-1]

# Add a transaction with relevant info to the 'blockpool' - list of pending tx's. 

    def new_transaction(self, url, owner="UWE",info= "special information"):
        
        data = {
            'url': url,
            'owner': owner,
            'info': info
        }
        #self.pending_data.append(data)
        self.pending_data=data
        return self.get_previous_block['index'] + 1

# receive one block. Turn it into a string, turn that into Unicode (for hashing). Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.

    def hashkeep(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        # return hashlib.sha256(block).hexdigest()
   
    def proof_of_work(self, previous_proof):
        # miners proof submitted
        new_proof = 1
        # status of proof of work
        check_proof = False
        while check_proof is False:
            # problem and algorithm based off the previous proof and new proof
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # check miners solution to problem, by using miners proof in cryptographic encryption
            # if miners proof results in 4 leading zero's in the hash operation, then:
            if hash_operation[:5] == '00000':# the number of zeros determines complexity
                check_proof = True
            else:
                # if miners solution is wrong, give mine another chance until correct
                new_proof += 1
                
        return new_proof

    def is_chain_valid(self, chain):
        # get the first block in the chain and it serves as the previous block
        previous_block = chain[0]
        # an index of the blocks in the chain for iteration
        block_index = 1
        while block_index < len(chain):
            # get the current block
            block = chain[block_index]
            # check if the current block link to previous block has is the same as the hash of the previous block
            if block["previous_hash"] != self.hash(previous_block):
                return False

            # get the previous proof from the previous block
            previous_proof = previous_block['proof']

            # get the current proof from the current block
            current_proof = block['proof']

            # run the proof data through the algorithm
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # check if hash operation is invalid
            if hash_operation[:5] != '00000':
                return False
            # set the previous block to the current block after running validation on current block
            previous_block = block
            block_index += 1
        return True
