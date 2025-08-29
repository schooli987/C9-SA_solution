import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize camera
cap = cv2.VideoCapture(0)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
print(width, height)

# MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Screen size
screen_width, screen_height = pyautogui.size()

# Variables
click_threshold = 40
screen_x, screen_y = 0, 0

def get_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

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

            # Mouse movement
            if abs(screen_x - screen_width * index_x / width) > 10 and abs(screen_y - screen_height * index_y / height) > 10:
                screen_x = screen_width * index_x / width
                screen_y = screen_height * index_y / height
                pyautogui.moveTo(screen_x, screen_y)

                # Left click (pinch thumb + index)
            if get_distance(index_x, index_y, thumb_x, thumb_y) < click_threshold:
                    pyautogui.click()
                    time.sleep(0.2)  # Avoid multiple clicks

                # Right click (pinch thumb + middle)
            if get_distance(middle_x, middle_y, thumb_x, thumb_y) < click_threshold:
                    pyautogui.click(button='right')
                    time.sleep(0.2)

                # Scroll up gesture
        if (landmarks[8].y > landmarks[6].y and  
                    landmarks[12].y > landmarks[10].y and
                    landmarks[16].y > landmarks[14].y and  
                    landmarks[20].y > landmarks[18].y and 
                    (landmarks[4].y < landmarks[0].y)):
                    pyautogui.scroll(50) 
                    time.sleep(0.2)
                
                # Scroll down gesture
        if (landmarks[8].y > landmarks[6].y and  
                    landmarks[12].y > landmarks[10].y and
                    landmarks[16].y > landmarks[14].y and  
                    landmarks[20].y > landmarks[18].y and 
                    (landmarks[4].y > landmarks[0].y)):
                    pyautogui.scroll(-50) 
                    time.sleep(0.2)

    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
