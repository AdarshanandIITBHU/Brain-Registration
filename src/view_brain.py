import viser
import socket
import threading
import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REGISTERED_MODEL = PROJECT_ROOT / "assets" / "brain_tumor_registered.glb"
ORIGINAL_MODEL = PROJECT_ROOT / "assets" / "brain_tumor_ar.glb"

MODEL_PATH = REGISTERED_MODEL if REGISTERED_MODEL.exists() else ORIGINAL_MODEL

print(f"Loading model: {MODEL_PATH.name}")

server = viser.ViserServer(port=8081)

with open(MODEL_PATH, "rb") as f:
    glb_data = f.read()

brain = server.scene.add_glb(
    "/brain",
    glb_data=glb_data,
    position=(0.0, 0.0, 0.0)
)

server.gui.add_markdown("### Brain Position Controls")

x_slider = server.gui.add_slider(
    "X Position", min=-0.2, max=0.2,
    step=0.001, initial_value=0.0
)
y_slider = server.gui.add_slider(
    "Y Position", min=-0.2, max=0.2,
    step=0.001, initial_value=0.0
)
z_slider = server.gui.add_slider(
    "Z Position", min=-0.2, max=0.2,
    step=0.001, initial_value=0.0
)

manual_control = {"enabled": True}

def update_position(_):
    if manual_control["enabled"]:
        brain.position = (
            x_slider.value,
            y_slider.value,
            z_slider.value
        )

x_slider.on_update(update_position)
y_slider.on_update(update_position)
z_slider.on_update(update_position)

reset = server.gui.add_button("Reset Position")

@reset.on_click
def reset_position(_):
    manual_control["enabled"] = True
    x_slider.value = 0.0
    y_slider.value = 0.0
    z_slider.value = 0.0
    brain.position = (0.0, 0.0, 0.0)

def receive_pose():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    print("Waiting for AprilTag pose data on UDP port 5005...")

    while True:
        try:
            data, _ = sock.recvfrom(4096)
            pose = json.loads(data.decode("utf-8"))

            manual_control["enabled"] = False

            brain.position = tuple(pose["position"])
            brain.wxyz = tuple(pose["rotation"])

        except Exception as error:
            print("Pose receiver error:", error)

threading.Thread(target=receive_pose, daemon=True).start()

print("Brain viewer running!")
print("Open http://localhost:8081")
print("UDP port: 5005")

while True:
    time.sleep(1)
