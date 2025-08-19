import asyncio
import base64
import json
import socket
import threading
import mediapipe as mp
import cv2
import numpy as np
import websockets

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # For drawing landmarks and connections
WRIST = 0
FINGER_TIPS = [8, 12, 16, 20]   # Index, Middle, Ring, Pinky tips
FINGER_PIPS = [6, 10, 14, 18]   # Corresponding PIP joints
async def receive_image_server(websocket):
    try:
        async for message in websocket:
            data = np.frombuffer(message, dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if image is not None:
                print("Received image", image.shape)
                _, cg = findFingers(image)
                await websocket.send(str(cg[0]) if cg else "No hands detected")
                cv2.imshow("Server Image", image)
                cv2.waitKey(1)
            else:
                print("Failed to decode image")
            await websocket.send("No hands detected")


    except Exception as e:
        print(f"Error receiving image: {e}")
def is_hand_open(hand_landmarks, h, w):
    open_count = 0
    wrist = hand_landmarks.landmark[WRIST]
    wrist_pos = np.array([wrist.x * w, wrist.y * h])

    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        tip_pos = np.array([hand_landmarks.landmark[tip].x * w,
                            hand_landmarks.landmark[tip].y * h])
        pip_pos = np.array([hand_landmarks.landmark[pip].x * w,
                            hand_landmarks.landmark[pip].y * h])

        # Distances from wrist
        d_tip = np.linalg.norm(tip_pos - wrist_pos)
        d_pip = np.linalg.norm(pip_pos - wrist_pos)

        if d_tip > d_pip:
            open_count += 1

    return open_count >= 4

def findFingers(frame, draw=True):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    centers = []

    if results.multi_hand_landmarks:
        h, w, _ = frame.shape
        for hand_landmarks in results.multi_hand_landmarks:
            if is_hand_open(hand_landmarks, h, w):
                xs = [lm.x * w for lm in hand_landmarks.landmark]
                ys = [lm.y * h for lm in hand_landmarks.landmark]
                cx, cy = int(np.mean(xs)), int(np.mean(ys))
                centers.append((cx, cy))

                if draw:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
                    cv2.putText(frame, f"({cx},{cy})", (cx + 10, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.arrowedLine(frame, (640 // 2, 480 // 2), (cx, cy), (0, 255, 255), 3, tipLength=0.1)

    return frame, centers




async def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    async with websockets.serve(receive_image_server, f"{ip}", 8765):
        print(f"Server running at ws://{ip}:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    # threading.Thread(target=show_frame()).start()
    asyncio.run(main())
    # asyncio.run(run_app())