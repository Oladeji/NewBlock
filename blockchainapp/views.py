import os
from django.shortcuts import render
from UWEBlockChainProj.settings import BASE_DIR, MEDIA_URL

from blockchainapp.QrCodegenerator import generateqrcode
from django.urls import path
from . Blockchain import Blockchain

def index(request):
    context={}
    if request.method =='POST' :
        
        url = request.POST['URL']
        owner=request.POST['OWNER']
        info=request.POST['INFOS']
        
      

        blockchain = Blockchain()

        t1 = blockchain.new_transaction(url, owner, info)
        previous_block = blockchain.get_previous_block
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
       
        print(proof)
        block,filename = blockchain.create_new_block(proof,previous_hash)

        context["filename"]=  MEDIA_URL+filename
      

        # t6 = blockchain.new_transaction("www.hotmail.com", "hotmail", '3')
        # previous_block = blockchain.get_previous_block
        # previous_proof = previous_block['proof']
        # proof = blockchain.proof_of_work(previous_proof)

        # print(proof)
        # previous_hash = blockchain.hash(previous_block)
        # block = blockchain.create_new_block(proof,previous_hash)

       
        # print("This is the block")

        for eachblock in blockchain.chain :
            print("*********creating new block*************************")
            print(eachblock)
            
            print("*********creating new block*************************")
        context.update(block)
      
    return render(request, 'index.html', context=context)