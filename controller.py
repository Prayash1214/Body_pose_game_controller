import cv2
import mediapipe as mp
import time 
import pyautogui
import os 


cap = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils




prev_x = None
prev_y = None
last_time = time.time()
cooldown = 0.6 



while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w , c = frame.shape
    result = pose.process(rgb)
    current_time=time.time()

    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        lm=result.pose_landmarks.landmark
        nose=lm[0]
        nx,ny=int(nose.x*w),int(nose.y*h)
        if prev_x is not None and prev_y is not None:
            dx = nx - prev_x
            dy = ny - prev_y
            if current_time - last_time > cooldown:
                    if abs(dy) > 10 and abs(dy) > abs(dx):
                        if dy < 5:
                            print("Up swipe -> W")
                            pyautogui.press('w')
                            last_time = current_time
                        elif dy > 0:
                            print("Down swipe -> S")
                            pyautogui.press('s')
                            last_time = current_time
                    elif abs(dx) > 10:
                        if dx > 0:
                            print("Right swipe -> D")
                            pyautogui.press('d')
                            last_time = current_time
                        else:
                            print("Left swipe -> A")
                            pyautogui.press('a')
                            last_time = current_time

    prev_x, prev_y = nx, ny 
            

        
      
        


        
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) &0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
