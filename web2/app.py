# app.py
from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/launch', methods=['POST'])
def launch():
    pkg = request.form['package']
    launch_file = request.form['launch_file']
    cmd = ["ros2", "launch", pkg, launch_file]
    subprocess.Popen(cmd)
    return jsonify(status=f"Launched {pkg}/{launch_file}")

@app.route('/start_rosbag', methods=['POST'])
def start_rosbag():
    cmd = ["ros2", "bag", "record", "-a"]  # Enregistre tous les topics
    subprocess.Popen(cmd)
    return jsonify(status="Started rosbag recording")

@app.route('/stop_rosbag', methods=['POST'])
def stop_rosbag():
    cmd = ["pkill", "-f", "ros2 bag record"]
    subprocess.Popen(cmd)
    return jsonify(status="Stopped rosbag recording")

if __name__ == '__main__':
    app.run(debug=True)
