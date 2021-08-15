from flask import Flask, render_template, Response
import cv2

app=Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0) #capture the video from laptop webcam
    #while loop to continuously capture the frames from the video and display on screen
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:

            #create detectors based on the haarcascade xmls
            face_cascade=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade=cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')

            #detect faces using the cascade created
            faces=face_cascade.detectMultiScale(frame,1.1,7)

            #create a gray version of image
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            #Draw rectangle aroud each face
            for(x,y,w,h) in faces:
                #draw rectangle around the face
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

                #create smaller gray image for eye detection
                roi_gray=gray[y:y+h, x:x+w]
                roi_color=frame[y:y+h, x:x+w]

                #detect eyes based on the cascade created
                eyes = eye_cascade.detectMultiScale(roi_gray,1.1,3)

                #draw rectangle around each eye
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            # below code takes the frame and converts into a buffer that can be displayed on screen
            ret, buffer = cv2.imencode('.jpg', frame)
            # convert buffer to bytes
            frame_bytes = buffer.tobytes()

        # yield is used instead of return as we want data to be sent every time loop runs. return will send once and exit.
        # arguements for yield is not clear to me.
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+frame_bytes+b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    #return "Inside video"
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)