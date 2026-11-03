import csv
import sys
import numpy as np
import trimesh
from pathlib import Path
from registration import estimate_rigid_transform

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "assets" / "landmarks.csv"
INPUT_GLB = ROOT / "assets" / "brain_tumor_ar.glb"
OUTPUT_GLB = ROOT / "assets" / "brain_tumor_registered.glb"
OUTPUT_TRANSFORM = ROOT / "assets" / "mri_to_head_transform.npz"

if not CSV_FILE.exists():
    sys.exit("Missing assets/landmarks.csv")

with CSV_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))

if len(rows) < 3:
    sys.exit("Add at least 3 corresponding, non-collinear landmarks to landmarks.csv.")

columns = [
    "mri_x", "mri_y", "mri_z",
    "head_x", "head_y", "head_z"
]

try:
    mri = np.array([[float(row[c]) for c in columns[:3]] for row in rows])
    head = np.array([[float(row[c]) for c in columns[3:]] for row in rows])
except (ValueError, KeyError):
    sys.exit("Invalid CSV. Fill all six coordinate columns with numbers.")

R, t, error = estimate_rigid_transform(mri, head)

T = np.eye(4)
T[:3, :3] = R
T[:3, 3] = t

scene = trimesh.load(INPUT_GLB, force="scene")
scene.apply_transform(T)
scene.export(OUTPUT_GLB)

np.savez(
    OUTPUT_TRANSFORM,
    rotation=R,
    translation=t,
    transform=T,
    rms_error=error
)

print("\nREGISTRATION COMPLETE")
print("Landmarks:", len(mri))
print("RMS error:", error)
print("Registered model:", OUTPUT_GLB)
print("Saved transform:", OUTPUT_TRANSFORM)
