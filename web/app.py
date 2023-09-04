# app.py
from flask import Flask, request, jsonify, render_template
import rclpy
from std_msgs.msg import String
import threading

app = Flask(__name__)

node = None
publisher = None
keep_running = False

def start_node():
    global node, publisher, keep_running
    rclpy.init()
    node = rclpy.create_node('my_node')
    publisher = node.create_publisher(String, 'topic', 10)
    msg = String()
    msg.data = "Hello, ROS2"

    keep_running = True
    while keep_running and rclpy.ok():
        publisher.publish(msg)
        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_node', methods=['POST'])
def start():
    global keep_running
    if not keep_running:
        threading.Thread(target=start_node).start()
        return jsonify(status="Node started")
    else:
        return jsonify(status="Node already running")

@app.route('/stop_node', methods=['POST'])
def stop():
    global keep_running
    keep_running = False
    return jsonify(status="Node stopped")

if __name__ == '__main__':
    app.run(debug=True)
