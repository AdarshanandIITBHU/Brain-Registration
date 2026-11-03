
"""Rigid registration from MRI coordinates to AprilTag coordinates.

Convention:
    point_tag = R_tag_from_mri @ point_mri + t_tag_from_mri
All coordinates must use the same physical unit (preferably metres).
"""

import numpy as np


def estimate_rigid_transform(mri_points, tag_points):
    """Estimate the rigid transform mapping MRI points to tag-frame points.

    Args:
        mri_points: Nx3 corresponding points in MRI coordinates.
        tag_points: Nx3 corresponding points in AprilTag coordinates.

    Returns:
        R: 3x3 rotation matrix.
        t: 3-element translation vector.
        rms_error: Root-mean-square registration error.
    """
    A = np.asarray(mri_points, dtype=float)
    B = np.asarray(tag_points, dtype=float)

    if A.shape != B.shape or A.ndim != 2 or A.shape[1] != 3:
        raise ValueError("Both point sets must have the same Nx3 shape.")

    if len(A) < 3:
        raise ValueError("At least 3 corresponding points are required.")

    if not np.all(np.isfinite(A)) or not np.all(np.isfinite(B)):
        raise ValueError("Landmark coordinates must be finite numbers.")

    centroid_A = A.mean(axis=0)
    centroid_B = B.mean(axis=0)

    A_centered = A - centroid_A
    B_centered = B - centroid_B

    if np.linalg.matrix_rank(A_centered) < 2:
        raise ValueError("MRI landmarks must not all lie on one line.")

    if np.linalg.matrix_rank(B_centered) < 2:
        raise ValueError("Tag-frame landmarks must not all lie on one line.")

    H = A_centered.T @ B_centered
    U, _, Vt = np.linalg.svd(H)

    R = Vt.T @ U.T

    # Prevent a reflection (which would mirror the brain).
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    t = centroid_B - R @ centroid_A

    predicted = (R @ A.T).T + t
    errors = np.linalg.norm(predicted - B, axis=1)
    rms_error = float(np.sqrt(np.mean(errors ** 2)))

    return R, t, rms_error


def transform_points(points, R, t):
    """Transform Nx3 points from MRI coordinates into tag coordinates."""
    points = np.asarray(points, dtype=float)
    return (R @ points.T).T + t


def save_transform(filename, R, t, rms_error):
    """Save the registration transform."""
    np.savez(
        filename,
        rotation=R,
        translation=t,
        rms_error=rms_error,
    )


def load_transform(filename):
    """Load a previously saved registration transform."""
    data = np.load(filename)
    return data["rotation"], data["translation"], float(data["rms_error"])


if __name__ == "__main__":
    # Synthetic test: known 90-degree rotation and translation.
    mri = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ])

    known_R = np.array([
        [0.0, -1.0, 0.0],
        [1.0,  0.0, 0.0],
        [0.0,  0.0, 1.0],
    ])
    known_t = np.array([0.2, 0.3, 0.4])

    tag = (known_R @ mri.T).T + known_t

    R, t, error = estimate_rigid_transform(mri, tag)

    print("Rotation:\n", R)
    print("Translation:", t)
    print("RMS error:", error)

    assert np.allclose(R, known_R, atol=1e-6)
    assert np.allclose(t, known_t, atol=1e-6)
    assert error < 1e-6

    print("\nRegistration test passed!")
