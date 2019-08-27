from flask import Flask 
from imutils.video import VideoStream
from flask import render_template, Response
import cv2
from myAlgoritm import MyAlgoritm

algo = MyAlgoritm()
app = Flask(__name__)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
def index():
     return render_template('imshow.html')

def get_frame():
    while True:
        im = algo.read()
        imgencode = cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    
@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    algo.start()
    app.run(host='0.0.0.0', port=5000)
    algo.stop()
    algo.join()