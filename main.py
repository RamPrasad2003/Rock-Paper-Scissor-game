''' IMPORTING NECCESARY PACKAGES AND MODULES'''
import cv2
import cvzone
from cvzone.HandTrackingModule  import HandDetector
import time
import random
''' VIDEO CAPTURING'''
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
'''HAND DETECTION'''
detector=HandDetector(maxHands=1)
'''INTIAL VARIABLES'''
timer=0
stateResult=False
startGame=False
playerMove=0
scores=[0,0]
'''LOOP FOR INFINITE CAPTURING'''
while True:
    '''TAKING BG.PNG AS BACKGROUND IMAGE'''
    BgImg=cv2.imread('./images/BG.png')

    success,img=cap.read()
    '''ADJUSTING THE CAPUTURED IMAGE'''
    imgScaled=cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled=imgScaled[:,80:480]
    '''DETECTING THE HAND GESTURES IN ADJUSTED VIDEO CAPTURE'''
    hands,img=detector.findHands(imgScaled)
    if startGame:
        if stateResult is False:
            '''TIMER COUNTDOWN'''
            timer=time.time()-initTime
            cv2.putText(BgImg,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)
            if timer>3:
                stateResult=True
                timer=0
                '''TYPE OF HAND GESTURE(ROCK,PAPER,SCISSOR)'''
                if hands:
                    hand=hands[0]
                    fingers=detector.fingersUp(hand)
                    if fingers==[0,0,0,0,0]:
                        playerMove=1            #ROCK
                    if fingers==[1,1,1,1,1]:
                        playerMove=2            #PAPER
                    if fingers==[0,1,1,0,0]:
                        playerMove=3            #SCISSOR
                    print(fingers)
                    '''TAKING RANDOM AI GESTURE'''
                    rNum=random.randint(1,3)
                    '''PLACING AI GESTURE IN MAIN FRAME'''
                    imgAI=cv2.imread(f'./images/{rNum}.png',cv2.IMREAD_UNCHANGED)
                    BgImg=cvzone.overlayPNG(BgImg,imgAI,(149,310))
                    #PLAYER WINS
                    if(playerMove==1 and  rNum==3) or (playerMove==2 and  rNum==1) or (playerMove==3 and  rNum==2):
                        scores[1]+=1
                    # AI WINS
                    if(playerMove==1 and  rNum==2) or (playerMove==2 and  rNum==3) or (playerMove==3 and  rNum==1):
                        scores[0]+=1
                    
    
    BgImg[234:654,795:1195]=imgScaled
    '''SHOWING AI GESTURE CONTINOUSLY IN BG IMAGE'''
    if stateResult:
        BgImg=cvzone.overlayPNG(BgImg,imgAI,(149,310))
    '''DISPLAYING SCORES IN RESPECTIVE PLACES'''
    cv2.putText(BgImg,str(scores[0]),(410,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.putText(BgImg,str(scores[1]),(1112,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.imshow('BG',BgImg)
    key=cv2.waitKey(1)
    '''IF YOU WANT TO START THEN PRESS 's' LETTER IN THE KEYBOARD '''
    if key==ord('s'):
        startGame=True
        initTime=time.time()
        stateResult=False
    '''BREAKING THE INFINITE LOOP AND STOPS THE ENTIRE PROCESS'''
    if key==ord('z'):
        break
        