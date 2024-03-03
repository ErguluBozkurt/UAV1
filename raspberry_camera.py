import cv2
import time


cap = cv2.VideoCapture("/dev/video0")

width = int(cap.get(3))
height = int(cap.get(4))
print(width, height)

writer = cv2.VideoWriter("/home/raspberrypi/new_save.mp4", cv2.VideoWriter_fourcc(*"DIVX"), 20, (width, height)) 

while True:
    _, frame = cap.read()
    writer.write(frame)

    if(cv2.waitKey(10) & 0xFF == ord("q")):
        break

cap.release()
writer.release() 
cv2.destroyAllWindows()
