#Generated completely with ChatGPT. Please read carefully before using. 
#Srikanth Sugavanam, 15th April 2026. 

import cv2
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
CAMERA_INDEX = 0
USE_SUM = False   # True = sum, False = mean


# -----------------------------
# Capture initial frame
# -----------------------------
def initialize_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        raise Exception("Could not open webcam")

    return cap


# -----------------------------
# Select ROI once
# -----------------------------
def get_roi(cap):
    print("Press SPACE to capture frame for ROI selection")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Live Feed - Press SPACE", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # SPACE
            break

    cv2.destroyAllWindows()

    roi = cv2.selectROI("Select Spectrum ROI", frame, showCrosshair=True)
    cv2.destroyAllWindows()

    x, y, w, h = roi
    return x, y, w, h


# -----------------------------
# Extract spectrum
# -----------------------------
def extract_spectrum(frame, roi_coords):
    x, y, w, h = roi_coords
    roi = frame[y:y+h, x:x+w]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    if USE_SUM:
        spectrum = np.sum(gray, axis=0)
    else:
        spectrum = np.mean(gray, axis=0)

    return spectrum


# -----------------------------
# Main real-time loop
# -----------------------------
def run_spectrometer():
    cap = initialize_camera()
    roi_coords = get_roi(cap)

    print("Starting real-time spectrum. Press 'q' to quit.")

    # Setup live plot
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_xlabel("Pixel Position (x)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title("Real-Time Spectrum")
    ax.grid()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        spectrum = extract_spectrum(frame, roi_coords)

        x = np.arange(len(spectrum))

        # Update plot
        line.set_xdata(x)
        line.set_ydata(spectrum)
        ax.relim()
        ax.autoscale_view()

        plt.pause(0.001)

        # Show ROI on video
        x0, y0, w, h = roi_coords
        display = frame.copy()
        cv2.rectangle(display, (x0, y0), (x0+w, y0+h), (0, 255, 0), 2)
        cv2.imshow("Spectrometer Feed", display)

        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.ioff()
    plt.show()


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    run_spectrometer()
