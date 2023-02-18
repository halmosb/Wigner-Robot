import cv2
from flask import Flask, render_template, Response
from time import sleep

app = Flask(__name__)

@app.route('/index/')
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/index_js")
def index_js():
    return render_template("index_js.js")


@app.route('/video_feed')
def video_feed():
    vid = cv2.VideoCapture(0)

    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 128*5)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 72*5)
    def gen():
        success, frame_cv = vid.read()
        if not success:
            return "Some error occured :("
        _, buffer = cv2.imencode('.jpg', frame_cv)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        vid.release()
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # without the debug=True, the camera works?
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        #vid.release()
        cv2.destroyAllWindows()
        print("exit")