import cv2
from flask import Flask, render_template, Response
from time import sleep
  
# define a video capture object
vid = cv2.VideoCapture(0)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, 128*5)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 72*5)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            success, frame_cv = vid.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame_cv)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            sleep(0.04)
        vid.release()
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    
    cv2.destroyAllWindows()