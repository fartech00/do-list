import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Streamlit UI
st.title("🖐️ Hand Tracking with Index Finger Line")

# Sidebar options
st.sidebar.header("Settings")
max_num_hands = st.sidebar.slider("Max Hands", 1, 2, 1)
detection_confidence = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.5)
tracking_confidence = st.sidebar.slider("Tracking Confidence", 0.1, 1.0, 0.5)

# Clear trail button
if st.sidebar.button("Clear Trail"):
    st.session_state.trail = deque(maxlen=1000)

# Video Capture
cap = cv2.VideoCapture(0)

# Initialize Hand Detector
hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=tracking_confidence
)

# Store index fingertip path (Landmark 8)
if "trail" not in st.session_state:
    st.session_state.trail = deque(maxlen=1000)  # Store last 1000 points

# Streamlit Video Capture
stframe = st.empty()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        st.warning("Could not read from webcam. Exiting...")
        break

    # Convert BGR to RGB (for MediaPipe processing)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    # Convert back to BGR (for OpenCV display)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Draw landmarks and track index fingertip
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index fingertip coordinates (Landmark 8)
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Add the fingertip position to the trail
            st.session_state.trail.append((x, y))

    # Draw the fingertip trail
    for i in range(1, len(st.session_state.trail)):
        if st.session_state.trail[i - 1] and st.session_state.trail[i]:
            cv2.line(frame, st.session_state.trail[i - 1], st.session_state.trail[i], (0, 255, 0), 3)

    # Display the frame in Streamlit
    stframe.image(frame, channels="BGR", use_column_width=True)

# Release resources
cap.release()
cv2.destroyAllWindows()
