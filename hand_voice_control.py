import cv2
import mediapipe as mp
import serial
import time
import threading
import speech_recognition as sr

# إعداد MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# الاتصال بالأردوينو
arduino = serial.Serial('COM6', 9600)
time.sleep(2)

# دالة عد الأصابع
def count_raised_fingers(landmarks, hand_label='Right'):
    finger_tips = [8, 12, 16, 20] 
    thumb_tip = 4
    count = 0

    if hand_label == 'Right':
        if landmarks[thumb_tip].x < landmarks[thumb_tip - 2].x:
            count += 1
    else:  # Left hand
        if landmarks[thumb_tip].x > landmarks[thumb_tip - 2].x:
            count += 1

    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1

    return count

# المتغيرات العامة
last_sent_time = 0
cooldown = 1
last_command = None
lock = threading.Lock()

# إرسال أمر للأردوينو
def send_command(command):
    global last_sent_time, last_command
    with lock:
        current_time = time.time()
        if current_time - last_sent_time > cooldown or last_command != command:
            arduino.write((command + '\n').encode())
            print(f"Command sent: {command}")
            last_command = command
            last_sent_time = current_time

# تفعيل الأوامر الصوتية
def voice_control():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            print("🎤 Listening for voice command...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio, language='ar-EG').lower()
                print("Heard:", command)

                # أوامر تشغيل/إيقاف عامة
                if "شغل" in command or "start" in command or "begin" in command or "on" in command:
                    send_command("on")
                elif "اطفي" in command or "stop" in command or "close" in command or "off" in command:
                    send_command("off")

                # أوامر حسب عدد الأصابع
                elif "صفر" in command or "0" in command or "زيرو" in command:
                    send_command("off")
                elif "واحد" in command or "1" in command:
                    send_command("led1")
                elif "اثنين" in command or "اتنين" in command or "2" in command or "وان" in command:
                    send_command("led2")
                elif "ثلاثة" in command or "تلاته" in command or "3" in command or "تلاتة" in command or "تو" in command:
                    send_command("led3")
                elif "أربعة" in command or "اربعه" in command or "4" in command or "ثري" in command:
                    send_command("led4")
                elif "خمسة" in command or "5" in command or "خمسه" in command or "فور" in command:
                    send_command("on")

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Dont got it!")
            except sr.RequestError as e:
                print("problem : ", e)


# تشغيل خيط الأوامر الصوتية
threading.Thread(target=voice_control, daemon=True).start()

# تشغيل الكاميرا
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_raised_fingers(hand_landmarks.landmark)
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            # إرسال أمر بناءً على عدد الأصابع
            if finger_count == 0:
                send_command("off")
            elif finger_count == 1:
                send_command("led1")
            elif finger_count == 2:
                send_command("led2")
            elif finger_count == 3:
                send_command("led3")
            elif finger_count == 4:
                send_command("led4")
            elif finger_count == 5:
                send_command("on")

    cv2.imshow("Hand + Voice Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
