
import viser
import socket
import threading
import json
import time
from pathlib import Path

# Resolve project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "assets" / "brain_tumor_ar.glb"

# Start the 3D viewer
server = viser.ViserServer(port=8081)

# Load the brain model
with open(MODEL_PATH, "rb") as f:
    glb_data = f.read()

brain = server.scene.add_glb(
    "/brain",
    glb_data=glb_data,
    position=(0.0, 0.0, 0.0)
)

# Position controls
server.gui.add_markdown("### Brain Position Controls")

x_slider = server.gui.add_slider(
    "X Position", min=-100.0, max=100.0,
    step=0.1, initial_value=0.0
)

y_slider = server.gui.add_slider(
    "Y Position", min=-100.0, max=100.0,
    step=0.1, initial_value=0.0
)

z_slider = server.gui.add_slider(
    "Z Position", min=-100.0, max=100.0,
    step=0.1, initial_value=0.0
)

def update_position(_):
    brain.position = (
        x_slider.value,
        y_slider.value,
        z_slider.value
    )

x_slider.on_update(update_position)
y_slider.on_update(update_position)
z_slider.on_update(update_position)

# Reset button
reset = server.gui.add_button("Reset Position")

@reset.on_click
def reset_position(_):
    x_slider.value = 0.0
    y_slider.value = 0.0
    z_slider.value = 0.0
    brain.position = (0.0, 0.0, 0.0)

# Receive AprilTag pose over UDP
def receive_pose():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    print("Waiting for AprilTag pose data on port 5005...")

    while True:
        try:
            data, _ = sock.recvfrom(4096)
            pose = json.loads(data.decode("utf-8"))

            brain.position = tuple(pose["position"])
            brain.wxyz = tuple(pose["rotation"])

        except Exception as error:
            print("Pose receiver error:", error)

threading.Thread(
    target=receive_pose,
    daemon=True
).start()

print("Brain viewer running!")
print("Open http://localhost:8081")
print("UDP port: 5005")

while True:
    time.sleep(1)
