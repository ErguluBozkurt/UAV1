import RPi.GPIO as GPIO
import cv2
import math
import numpy as np
from ultralytics import YOLO

# Servo pin tanımları
left_right_pin = 11
up_down_pin = 13

# Servo açı aralıkları
left_right_min_angle = 0
left_right_max_angle = 180
up_down_min_angle = 0
up_down_max_angle = 180

# Servo pinlerinin başlangıç durumu
left_right_angle = 90
up_down_angle = 90

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_right_pin, GPIO.OUT)
GPIO.setup(up_down_pin, GPIO.OUT)

# PWM frekans ve duty cycle ayarı
pwm_left_right = GPIO.PWM(left_right_pin, 50)
pwm_up_down = GPIO.PWM(up_down_pin, 50)
pwm_left_right.start(0)
pwm_up_down.start(0)

# Servo hareket fonksiyonu
def move_gimbal(left_right_angle, up_down_angle):
    left_right_duty = left_right_angle / 18 + 2
    up_down_duty = up_down_angle / 18 + 2
    pwm_left_right.ChangeDutyCycle(left_right_duty)
    pwm_up_down.ChangeDutyCycle(up_down_duty)

video_path = "car_video.mp4"
model_path = "best.pt"

cap = cv2.VideoCapture(video_path)
model = YOLO(model_path)

while True:
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
        results = model.track(frame, persist=True, verbose=False)[0]
        
        bboxes = np.array(results.boxes.data.tolist(), dtype="int")
        
        for box in bboxes:
            x, y, x1, y1, _, _, _ = box
            w = x1 - x
            h = y1 - y 
            cx, cy = x + w // 2, y + h // 2
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

            cx2, cy2 = 1280 // 2, 720 // 2
            cv2.circle(frame, (cx2, cy2), 5, (255, 0, 255), -1)

            cv2.line(frame, (cx2, cy2), (cx, cy), (255, 0, 0), 1)

            s = round(math.sqrt(math.pow(cx2 - cx, 2) + math.pow(cy2 - cy, 2)), 2)
            cv2.putText(frame, f"Mesafe : {s}", (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

            if cx <= 640 and cy <= 360:
                text = "Left-Up"
            elif cx <= 640 and cy > 360:
                text = "Left-Down"
            elif cx > 640 and cy <= 360:
                text = "Right-Up"
            elif cx > 640 and cy > 360:
                text = "Right-Down"
            else:
                text = "Tespit Edilemedi"

            cv2.putText(frame, f"Bilgi : {text}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

            # Servo hareketini hesapla
            left_right_angle += int((cx - cx2) / 10)
            up_down_angle += int((cy - cy2) / 10)
            left_right_angle = max(0, min(180, left_right_angle))
            up_down_angle = max(0, min(180, up_down_angle))

            # Servo hareketini gerçekleştir
            move_gimbal(left_right_angle, up_down_angle)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Okuma Hatası")
        break

cap.release()
cv2.destroyAllWindows()
