import numpy as np
import cv2

#enable webcam for imagedetection
#'0' default for internal webcam

liveImg = cv2.VideoCapture(0);

liveImg.set(3, 640);
liveImg.set(4, 480);

while True :

    # Capture the video frame
    # by frame
    success, img = liveImg.read();

    # Display the resulting frame
    cv2.imshow('frame', img);

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
liveImg.release();
# Destroy all the windows
cv2.destroyAllWindows();