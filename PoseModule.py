import cv2
import mediapipe as mp
import time
import math
 
 
class poseDetector():
 
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
 
        # self.mode = mode
        # self.upBody = upBody
        # self.smooth = smooth
        # self.detectionCon = min_detection_confidence
        # self.trackCon = min_tracking_confidence
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
 
    def findPosition(self, img):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

        return self.lmList
 
    def findAngle(self, img, p1, p2, p3):
 
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
 
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        return angle

class FallDetector:
    def __init__(self) -> None:
        self.fall_position = (0, 0, 0)
        self.fall_count = 0
        pass
    
    def update(self, frame_count, head, top, bot):
        if frame_count == 0:
            self.fall_position = (head, top, bot)
            print(self.fall_position[1])
            print(self.fall_position[2])
        else:
            if self.fall_position[0] != 0:
                if (2*float(self.fall_position[0][2]) < float(head[2])):
                    if (abs(top[1]-bot[1]) > 1.5*(abs(self.fall_position[1][1] - self.fall_position[2][1])) and 
                        abs(top[2]-bot[2]) < 0.3 * abs(self.fall_position[1][2] - self.fall_position[2][2])):
                        self.fall_count += 1
                        print("=============")
                        print(top[2])
                        print(bot[2])
                        self.fall_position = (head, top, bot)
        return self.fall_count
 
# def main():
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     detector = poseDetector()
#     while True:
#         success, img = cap.read()
#         img = detector.findPose(img)
#         lmList = detector.findPosition(img)

#         if len(lmList) != 0:
#             print(lmList[14])
#             cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

#         #print time, dps
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
 
#         cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                     (255, 0, 0), 3)
 
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
 
 
# if __name__ == "__main__":
#     main()