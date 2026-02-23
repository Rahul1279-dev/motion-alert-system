import cv2, time, os, glob
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0) # Creating an object instance
# NOTE:
# If you are using your inbuild laptop camera then use '0'
# If you are using external camera, e.g. USB Camera or any other 3rd party camera app then use '1'

time.sleep(1)

def clean_folder():
    print("Clean folder function started")

    images = glob.glob("Images/*.png")
    for image in images:
        os.remove(image)

    print("Clean folder function ended")

first_frame = None # Initializing the variable
status_list = []
count = 1
while True:
    status = 0 # Initializing the status variable in each iteration
    check, frame= video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (23, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000: # Will ignore those contours which have contour area less than 5,000 pixels
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            if 'Images' not in os.listdir():
                os.mkdir("Images")
            filepath = f"Images/image-{count}.png"
            cv2.imwrite(filepath, frame)
            count += 1
            all_images = glob.glob("Images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:] # Updating the list in each iteration with only last 2 items
    if status_list[0] == 1 and status_list[1] == 0: # Sending email only when the object is leaving the screen i.e. 1-->0
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

clean_thread.start()
video.release()