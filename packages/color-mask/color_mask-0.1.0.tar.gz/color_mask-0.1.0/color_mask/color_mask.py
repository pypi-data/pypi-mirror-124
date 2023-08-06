import numpy as np
import cv2
import argparse
import os

import color_mask

class clrmsk:
    def __init__(self):
        pass

    def stackImages(self, scale,imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range ( 0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor= np.hstack(imgArray)
            ver = hor
        return ver

    def empty(self, a):
        pass



def main():

    cm = clrmsk()

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    
    # if ap.task == 'data_cleaning':
    ap.add_argument('task', default=None, nargs='?', type=str, help="specifies the task that you want to perform")
    ap.add_argument("-p", "--img_path", help="provide path of image")
    args = ap.parse_args()
    
    task = str(args.task)
    if  task == 'createmsk':
        img = cv2.imread(args.img_path)
        # img = cv2.imread('/home/chinmay/Downloads/earphones.jpg')
        cv2.imshow("img",img)
        img = cv2.resize(img, (img.shape[1],img.shape[0]))

        cv2.namedWindow("trackBars")
        cv2.resizeWindow("trackBars",640,240)
        cv2.createTrackbar("Hue min", "trackBars", 0, 179, cm.empty)
        cv2.createTrackbar("Hue max", "trackBars", 179, 179, cm.empty)
        cv2.createTrackbar("Sat min", "trackBars", 148, 255, cm.empty)
        cv2.createTrackbar("Sat max", "trackBars", 231, 255, cm.empty)
        cv2.createTrackbar("Val min", "trackBars", 216, 255, cm.empty)
        cv2.createTrackbar("Val max", "trackBars", 255, 255, cm.empty)

        while True:
            imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hmin = cv2.getTrackbarPos("Hue min", "trackBars")
            hmax = cv2.getTrackbarPos("Hue max", "trackBars")
            smin = cv2.getTrackbarPos("Sat min", "trackBars")
            smax = cv2.getTrackbarPos("Sat max", "trackBars")
            vmin = cv2.getTrackbarPos("Val min", "trackBars")
            vmax = cv2.getTrackbarPos("Val max", "trackBars")
            print(hmin, hmax, smin, smax, vmin, vmax)
            lower = np.array([hmin,smin,vmin])
            upper = np.array([hmax,smax,vmax])
            mask = cv2.inRange(imgHsv, lower, upper)
            imgRes = cv2.bitwise_and(img,img,mask=mask)

            
            imgstack = cm.stackImages(0.8,([img,imgHsv],[mask,imgRes]))

            cv2.imshow("stacked",imgstack)
            
            k = cv2.waitKey(1)
            if k == 27:
                break

    if  args.task == 'savemsk':
        hmin = int(input("enter Hue min: "))
        hmax = int(input("enter Hue max: "))
        smin = int(input("enter Sat min: "))
        smax = int(input("enter Sat max: "))
        vmin = int(input("enter Val min: "))
        vmax = int(input("enter Val max: "))
        # img = cv2.imread('/home/chinmay/Downloads/earphones.jpg')
        img = cv2.imread(args.img_path)
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([hmin,smin,vmin])
        upper = np.array([hmax,smax,vmax])
        mask = cv2.inRange(imgHsv, lower, upper)
        imgRes = cv2.bitwise_and(img,img,mask=mask)
        cv2.imwrite("maskedImg.jpg",imgRes)
    
    if task == 'None':
        print("Hello there friend, this is our mini project!!")

    else: print("Sorry the required action cannot be performed, refer the docs for further guidance")



    

if __name__ == "__main__":
    main()