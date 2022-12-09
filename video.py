import numpy as np
import cv2

#enable webcam for imagedetection
#'0' default for internal webcam
liveImg = cv2.VideoCapture(0)

liveImg.set(3, 640)
liveImg.set(4, 480)

while True :

    #capture the video frame by frame
    success, img = liveImg.read()

    #display the resulting frame
    cv2.imshow('Fruit Detection', img)

    #the 'q' button is set as the
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#after the loop release the cap object
liveImg.release()

#destroy all the windows
cv2.destroyAllWindows()