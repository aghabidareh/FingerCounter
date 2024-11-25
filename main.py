import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

def countFingers(handLandmarks):
    landmarks = handLandmarks.landmark
    fingers = []

    isRightHand = landmarks[17].x > landmarks[5].x

    if(isRightHand and landmarks[4].x < landmarks[3].x) or (not isRightHand and landmarks[4].x > landmarks[3].x):
        fingers.append(1)
    else:
        fingers.append(0)

    for tipID in [8, 12, 16, 20]:
        if landmarks[tipID].y < landmarks[tipID - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

cap = cv2.VideoCapture(0)
with mpHands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9 , max_num_hands=2) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgbFrame)
        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)

                totalFingers = countFingers(handLandmarks)

                x = int(handLandmarks.landmark[0].x * frame.shape[1])
                y = int(handLandmarks.landmark[0].x * frame.shape[0])
                cv2.putText(frame , f'{totalFingers}', (x, y - 20),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,(0,255,0) , 3)

        cv2.imshow('Finger Counter', frame)\

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()