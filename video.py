import cv2

import asyncio
import websockets

import json

async def detect(websocket):
    #classifier for banana
    banacascade=cv2.CascadeClassifier('classifier/banana_classifier.xml')

    #classifier for orange
    orangecascade=cv2.CascadeClassifier('classifier/orange_classifier.xml')

    #classifier for apple
    applecascade=cv2.CascadeClassifier('classifier/apple_classifier.xml')

    #enable webcam for imagedetection
    #'0' default for internal webcam
    liveImg = cv2.VideoCapture(0)

    fruit = None

    #set Window size
    liveImg.set(3, 640)
    liveImg.set(4, 480)

    isDetected = False

    while True :
        #capture the video frame by frame        
        success, img = liveImg.read()

        #image to grayscale
        grayScale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        banana=banacascade.detectMultiScale(grayScale,scaleFactor=1.4,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
        orange=orangecascade.detectMultiScale(grayScale,scaleFactor=1.2,minNeighbors=10,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
        apple=applecascade.detectMultiScale(grayScale,scaleFactor=1.6,minNeighbors=10,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

        for(x,y,w,h) in banana:
            #draw box around object, colorvalues in BGR
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
            #name frame, colorvalues in BGR
            cv2.putText(img,'Banana',(x-10,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,255))
            fruit = 'banana'
            isDetected = True

        for(x,y,w,h) in orange:
            #draw box around object, colorvalues in BGR
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
            #name frame, colorvalues in BGR
            cv2.putText(img,'Orange',(x-10,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,165,255))
            fruit = 'orange'
            isDetected = True

        for(x,y,w,h) in apple:
            #draw box around object, colorvalues in BGR
            #cv2.rectangle(img,(x,y),(x+w,y+h),(50,205,50),3)                
            #name frame, colorvalues in BGR
            cv2.putText(img,'Apple',(x-10,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(50,205,50)) 
            fruit = 'apple'
            isDetected = True

        

        if fruit is not None and isDetected:
            event = {
                "type": "detected",
                "fruit": fruit,
            }
            await websocket.send(json.dumps(event)) 
            isDetected = False
            fruit = None              

        #display the resulting frame
        cv2.imshow('Fruit Detection', img)


        #the 'q' button is set as the
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #after the loop release the cap object
    liveImg.release()

    #destroy all the windows
    cv2.destroyAllWindows()

async def main():
    async with websockets.serve(detect, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())   