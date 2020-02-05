import cv2
import datetime
import time
import copy

webcam = None
key = None
frame = None
size = (0, 0)


def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (255, 255, 255)
    thickness = -1#cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


def setup():
    print("setup")
    global webcam
    global key
    global size

    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    width = 1280
    height = 720
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    size = (width, height)
    print("Ready")
    startAppLoop()


def startAppLoop():
    global key
    global frame
    while True:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        try:
            key = cv2.waitKey(1)

            if key == ord("s"):
                takePicture()
                # setup()
            elif key == ord("q"):
                endProcess()
                break

        except (KeyboardInterrupt):
            endProcess()
            break
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break


def takePicture():
    global frame
    global webcam
    print("Take Picture")
    date = datetime.datetime.now()
    fileName = date.strftime("%d-%m-%Y-%H-%M-%S")
    imageFileName = "./Data/" + fileName + ".jpg"
    cv2.imwrite(filename=imageFileName, img=frame)
    print("Image saved!")
    takeVideo(fileName)


def takeVideo(fileName):
    global frame
    global webcam
    global size
    print("Take Video")
    videoFileName = "./Data/" + fileName + ".avi"

    # start
    #fourcc = cv2.cv.CV_FOURCC('M','P','E','G')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(videoFileName, fourcc, 20.0, size)
    videoLength = 5

    now = time.time()
    end = now + videoLength

    while time.time() < end:
        _, _frame = webcam.read()
        textFrame = copy.copy(_frame)
        #__draw_label(textFrame, "RECORDING", (25, 25), (0, 0, 0))
        cv2.imshow("Capturing", textFrame)
        out.write(_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # end
    print("Video saved!")


def endProcess():
    global webcam
    print("Turning off camera.")
    webcam.release()
    print("Camera off.")
    print("Program ended.")
    cv2.destroyAllWindows()


def postData():
    print("Make request")


setup()
