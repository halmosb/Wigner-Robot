from flask import Flask, redirect, url_for, request, render_template
import cv2
from time import sleep
import matplotlib.pyplot as plt

# define a video capture object
vid = cv2.VideoCapture(0)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, 128*5)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 72*5)



app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route('/video_feed')
def video_feed():
    success, frame_cv = vid.read()

    print(frame_cv)
    if not success:
        return "1"
    _, buffer = cv2.imencode('.jpg', frame_cv)
    frame = buffer.tobytes()

    return str(buffer)

@app.route("/")
def index():
    return "Hello"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    #vid.release()
