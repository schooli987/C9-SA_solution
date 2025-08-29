import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize camera
cap = cv2.VideoCapture(0)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

# MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Screen size
screen_width, screen_height = pyautogui.size()
screen_x, screen_y = 0, 0


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            landmarks = hand_landmarks.landmark
            index_x, index_y = int(landmarks[8].x * width), int(landmarks[8].y * height)
            thumb_x, thumb_y = int(landmarks[4].x * width), int(landmarks[4].y * height)
            middle_x, middle_y = int(landmarks[12].x * width), int(landmarks[12].y * height)
            
            # Draw pointer
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)

            # Move mouse
               
            new_x = screen_width * index_x / width
            new_y = screen_height * index_y / height

            if abs(screen_x - new_x) > 10 and abs(screen_y - new_y) > 10:
                screen_x, screen_y = new_x, new_y

                pyautogui.moveTo(screen_x, screen_y)

          

    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
