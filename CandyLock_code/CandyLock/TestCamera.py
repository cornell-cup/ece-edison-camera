import cv2
cap=cv2.VideoCapture(0)


try:
    while True:
        print "Press key to start"
        raw_input()
        cap.open(0)
        res,img=cap.read()
        cv2.imwrite("./camTest.jpg",img)
        cap.release()
        print "photo taken"
except KeyboardInterrupt:
    print "done"
    cap.release()
