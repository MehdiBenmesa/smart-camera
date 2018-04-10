from flask import Flask, render_template, Response, send_from_directory, jsonify, request
from classes import Camera, FaceRecognizer, PersonsDB
import cv2
import numpy
import os



app = Flask(__name__, template_folder='client')
face_recognizer = FaceRecognizer()
db = PersonsDB()
last_inserted_id = 0
try:
    camera
except NameError:
    camera = Camera(0)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register")
def register():
    return render_template('register.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        #frame = face_recognizer.predict(frame)
        ret, frame = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@app.route("/video")
def video():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/api/picture")
def take_picture():
    frame = camera.get_frame()
    return jsonify(cv2.imwrite('static/img/tmp.jpg', frame))


@app.route("/api/process")
def process():
    img = cv2.imread('static/img/tmp.jpg', cv2.IMREAD_COLOR)
    img, person = face_recognizer.predict(img, db)
    cv2.imwrite('static/img/tmp.jpg', img)
    return jsonify(person)


@app.route("/api/save", methods = ['POST'])
def save():
    global last_inserted_id
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    birthday = request.form.get('birthday')
    company = request.form.get('company')
    email = request.form.get('email')
    image = request.form.get('image')
    db.open()
    last_inserted_id = id = db.insert_person(firstName, lastName, birthday, email, company)
    #print(firstName, lastName, birthday, company, email, id)
    db.close()
    return jsonify(face_recognizer.save_face(str(id), camera))


@app.route("/api/upload", methods=['POST'])
def upload():
    global last_inserted_id
    image = request.files['file']
    image.save('static/img/'+str(last_inserted_id) +'.jpg')
    return True


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)


