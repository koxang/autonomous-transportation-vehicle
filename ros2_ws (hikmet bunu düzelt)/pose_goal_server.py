from flask import Flask, request
import serial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

app = Flask(__name__)

# UART ayarı
try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("[UART] ttyAMA0 bağlantısı kuruldu.")
except Exception as e:
    print(f"[UART ERROR] ttyAMA0 bağlantısı kurulamadı: {e}")
    ser = None

# ROS2 başlat
rclpy.init()
ros_node = rclpy.create_node('pose_goal_node')
publisher = ros_node.create_publisher(PoseStamped, '/goal_pose', 10)

def send_goal(x, y):
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.header.stamp = ros_node.get_clock().now().to_msg()
    goal.pose.position.x = x
    goal.pose.position.y = y
    goal.pose.orientation.w = 1.0  # düz yön
    publisher.publish(goal)
    print(f"[ROS2] /goal_pose gönderildi: x={x}, y={y}")

    if ser:
        msg = f"GIDILECEK_HEDEF: {x},{y}\n"
        ser.write(msg.encode())
        print(f"[UART] Gönderildi: {msg.strip()}")

@app.route('/receive_command', methods=['POST'])
def receive_command():
    try:
        data = request.json.get("command", "")
        print(f"[HTTP] Gelen komut: {data}")

        if data.startswith("START_AUTONOMOUS:"):
            coords = data.split(":")[1]
            x, y = map(float, coords.split(","))
            send_goal(x, y)
            return {"status": "ok", "received": f"{x},{y}"}
        else:
            return {"status": "ignored", "reason": "unknown command"}
    except Exception as e:
        print(f"[ERROR] Komut işlenemedi: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5250)
