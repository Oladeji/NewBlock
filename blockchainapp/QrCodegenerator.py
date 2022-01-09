import os
from UWEBlockChainProj.settings import MEDIA_ROOT
import qrcode 
import json
import cv2 
import random

def generateqrcode(data):
  #dicttostr= json.dumps(data)
  #print(dicttostr)
  img= qrcode.make(data)
  filename= "Myimage"+str(random.randint(1, 1000))+".png"
  filename2 =  os.path.join(MEDIA_ROOT, filename) 

  img.save(filename2)

  return img,filename

def decodeqrcode(img) :
    d= cv2.QRCodeDetector()
    dicttostr,point,qrcodestr =d.DetectAndDecode(cv2.imread(img))
    