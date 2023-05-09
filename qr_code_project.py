from threading import Thread
import cv2
import time
import numpy as np
from pyzbar import pyzbar
import os

#function to get Serial# from Jetson
try:
    serial_number = os.system('cat /proc/device-tree/serial-number')
except:
    print('cannot retrieve serial number from Jetson Device')
    
class vStream:
    def __init__(self,src):
        self.capture=cv2.VideoCapture(src)
        self.thread=Thread(target=self.update,args=())
        self.thread.daemon=True
        self.thread.start()
    def update(self):
        while True:
            _,self.frame=self.capture.read()
            
    def getFrame(self):
        return self.frame


def qr_decode(image):
    barcodes = pyzbar.decode(image)
    frame_count = 1
    # Step.4
    # loop over the detected barcodes
    for barcode in barcodes:
        print('decoding list of barcodes')
        print("[Barcode] starting analyze barcode %d ..." % frame_count)
        frame_count = frame_count + 1
        
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        print(text)    
        cv2.putText(image, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    return image


#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#Change the numerical value in the below function to where the USB camera is plugged in
cam1=vStream(0)

#Add in a second camera
cam2=vStream(2)


font=cv2.FONT_HERSHEY_SIMPLEX
startTime=time.time()
dtav=0
while True:
    try:
        myFrame1=cam1.getFrame()
        myFrame2=cam2.getFrame()
        barcodes1 = qr_decode(myFrame1)
        barcodes2 = qr_decode(myFrame2)
        dt=time.time()-startTime
        startTime=time.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        cv2.imshow('barcodes1',barcodes1)
        cv2.imshow('barcodes2',barcodes2)
 
    except:
        print('frame not availablqe')
        
    if cv2.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break
