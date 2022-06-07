import serial
import cv2
import mediapipe as mp

""" References: 
https://www.section.io/engineering-education/creating-a-finger-counter/#results
https://blog.eletrogate.com/como-conectar-o-arduino-com-o-python/ 
"""

class ArduinoLed(object):
    
    def __init__(self):
        pass

    def getHandNumberArduino(self)->any:
        result = ""
        resultTxt = ""
        gravarL = True
        gravarD = True
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils
        fingerCoord = [(8,6),(12,10),(16,14),(20,18)]
        thumbCoord = (4,2)        
        while True:
            success, image = cap.read()
            RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(RGB_image)
            multiLandMarks = results.multi_hand_landmarks
            if multiLandMarks:
                handList = []
                for handLms in multiLandMarks:
                    mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
                    for idx, lm in enumerate(handLms.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        handList.append((cx, cy))
                for point in handList:
                    cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
                    upCount = 0
                    for coordinate in fingerCoord:
                        if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                            upCount += 1
                    if handList[thumbCoord[0]][0] > handList[thumbCoord[1]][0]:
                        upCount += 1                   
                    if(upCount > 0):
                        result = 1
                        resultTxt = "Ligado"
                    else:
                        result = 0
                        resultTxt = "Desligado"
                    cv2.putText(image, resultTxt, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))                        
            cv2.imshow('Arduino Hands Led', image)
            if cv2.waitKey(1) & 0xff==ord('q'):
                break
            
            resultA = 'l' if result == 1 else 'd'          
            
            if resultA == 'l' and gravarL == True:
                arduino = serial.Serial('/dev/ttyACM0', 9600)
                arduino.write('l'.encode())
                gravarL = False
                gravarD = True
                arduino.flush()
            elif resultA == 'd' and gravarD == True:
                arduino = serial.Serial('/dev/ttyACM0', 9600)
                arduino.write('d'.encode())
                gravarD = False
                gravarL = True
                arduino.flush()
    
        cap.release()
        cv2.destroyWindow('Arduino Hands Led')

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    arduinoLed = ArduinoLed()
    arduinoLed.getHandNumberArduino()