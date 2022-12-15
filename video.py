import numpy as np
import cv2


#classifier for banana
banacascade=cv2.CascadeClassifier('banana_classifier.xml')

#enable webcam for imagedetection
#'0' default for internal webcam
liveImg = cv2.VideoCapture(0)

#set Window size
liveImg.set(3, 640)
liveImg.set(4, 480)

while True :

    #capture the video frame by frame
    success, img = liveImg.read()

    #image to grayscale
    grayScale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    banana=banacascade.detectMultiScale(grayScale,scaleFactor=1.3,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

    for(x,y,w,h) in banana:
        #draw box around object, colorvalues in BGR
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
        #name frame, colorvalues in BGR
        cv2.putText(img,'Banana',(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255))

    #display the resulting frame
    cv2.imshow('Fruit Detection', img)

    #the 'q' button is set as the
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#after the loop release the cap object
liveImg.release()

#destroy all the windows
cv2.destroyAllWindows()