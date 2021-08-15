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