import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)
ros_node = None
target_command = {"steer": 0, "speed": 0}
last_command_time = time.time()
lock = threading.Lock()

class DrivePublisher(Node):
    def __init__(self):
        super().__init__('manual_drive_node')
        self.publisher_ = self.create_publisher(Int16MultiArray, 'manual_drive_topic', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        print(">>> DrivePublisher başlatıldı!")

    def timer_callback(self):
        msg = Int16MultiArray()
        with lock:
            steer = target_command["steer"]
            speed = target_command["speed"]
            if time.time() - last_command_time > 1.0:
                steer = 0
                speed = 0
        msg.data = [steer, speed]
        self.publisher_.publish(msg)

@app.route('/control', methods=['POST'])
def control():
    global target_command, last_command_time
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing 'command' field in JSON"}), 400

    command = data["command"]
    print("Received command:", command)

    if isinstance(command, str):
        if command == "forward":
            steer = 0
            speed = 800
        elif command == "backward":
            steer = 0
            speed = -800
        elif command == "left":
            steer = -400
            speed = 600
        elif command == "right":
            steer = 400
            speed = 600
        elif command == "stop":
            steer = 0
            speed = 0
        else:
            steer = 0
            speed = 0
    elif isinstance(command, dict):
        steer = int(command.get("steer", 0))
        speed = int(command.get("speed", 0))
    else:
        return jsonify({"error": "Invalid command format. Must be string or dict."}), 400

    with lock:
        target_command["steer"] = steer
        target_command["speed"] = speed
        last_command_time = time.time()

    return jsonify({"status": "command updated"}), 200

def flask_thread():
    app.run(host='0.0.0.0', port=5000)

def main(args=None):
    print(">>> main() fonksiyonu başlıyor...")
    rclpy.init(args=args)
    drive_publisher = DrivePublisher()

    thread = threading.Thread(target=flask_thread)
    thread.daemon = True
    thread.start()

    try:
        rclpy.spin(drive_publisher)
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        drive_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

