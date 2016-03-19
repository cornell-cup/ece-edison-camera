'''
ImageRecognizer

This utility is used for recognizing objects in images by histogram

It works best when the background is clean and unicolored, the object is in 
a well-lit environment without external lighting.

'''
import cv2
import argparse
import numpy as np
import sys
import os
import re

dataDir="./trained/"

kernel=np.ones((20,20),np.uint8)

capture=cv2.VideoCapture(0)

counter=0

def getMask(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(gray,(3,3),0)
    #cv2.imwrite("/home/root/itl_imgRec_test0.png",blurred)
    edged = cv2.Canny(blurred, 70, 200)
    #cv2.imwrite("/home/root/itl_imgRec_test1.png",edged)
    morphed=cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    (cnts, _) = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height,width,depth=img.shape
    mask=np.zeros((height,width,1),np.uint8)    
    cv2.drawContours(mask,cnts,-1,(255,255,255),-1)
    return mask

def getHist_H(img):
    msk=getMask(img)
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hist=cv2.calcHist([img_hsv],[0],msk,[50],[0,180])
    cv2.normalize(hist,hist,0,1,cv2.NORM_MINMAX,-1)
    return hist

def getCapture(capture):
    capture.open(0)
    #capture.set(3,512)
    #capture.set(4,384)
    status, img=capture.read()
    capture.release()
    return img
    
def fromCapture(func):
    def inner(*args,**kwargs):
        global counter
        img=getCapture(capture)
        cv2.imwrite("./test/vcT%d.jpg"%counter,img)
        counter=counter+1
        return func(img=img,*args,**kwargs)
    return inner

@fromCapture
def init(*args,**kwargs):
    pass
    
@fromCapture
def train(num,img):
    fname=dataDir+"/rec%d.npy"%num
    hst=getHist_H(img)
    np.save(fname,hst)

@fromCapture    
def recognize(img):
    hst=getHist_H(img)
    results=[]
    for root,dirs,filenames in os.walk(dataDir):
      for one in filenames:
        hst_o=np.load(os.path.join(root,one))
        res=cv2.compareHist(hst_o,hst,0)
        #print (one,res)
        results.append((one,res))
    results=sorted(results,key=lambda a:a[1])
    result=results[-1]
    if result[1]<0.6:
        return -1
    else:
        return int(re.findall(r"\d+",result[0])[0])
    
if __name__=="__main__":
  ap=argparse.ArgumentParser()
  ap.add_argument("-t","--train",default=0)
  ap.add_argument("-r","--recognize",default=0)

  args=vars(ap.parse_args())

  train_src=args["train"]
  reco_src=args["recognize"]
  
  
  if train_src:
    train_id=int(train_src)
    train(train_id)
  
  if reco_src:
    res=recognize()
    print res
    

