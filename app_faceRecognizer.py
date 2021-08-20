from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np

app=Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0) #capture the video from laptop webcam
    
    #learn the known faces for cmparing to new ones

    # Load a sample picture and learn how to recognize it.
    abhishek_image = face_recognition.load_image_file("Images/abhishek.jpg")
    abhishek_face_encoding = face_recognition.face_encodings(abhishek_image)[0]
    
    # Load a second sample picture and learn how to recognize it.
    amitabh_image = face_recognition.load_image_file("Images/amitabh.jpg")
    amitabh_face_encoding = face_recognition.face_encodings(amitabh_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [abhishek_face_encoding,amitabh_face_encoding]
    known_face_names = ["abhishek","amitabh"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    #while loop to continuously capture the frames from the video and display on screen
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                name = "Unknown"
                
                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                name=known_face_names[best_match_index]    

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
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