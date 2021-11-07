
import cv2
import time
import schedule
import PoseModule as pm

# 'PoseVideos/videos_ADL/ADL-bending_.mp4'
cap = cv2.VideoCapture('PoseVideos\\videos_FALL\\FALL-Backwards_.mp4')
pTime = 0
detector = pm.poseDetector()
fall_detector = pm.FallDetector()
frame_count = 0
fall_count = 0

def recordTimer():
    global frame_count
    frame_count = 0

schedule.every(0.8).seconds.do(recordTimer)

while True:

    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # # 找點跟指定2點角度
    # if len(lmList) !=0:
    #     print(lmList[14])
    #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

    #     # get angle
    #     angle = detector.findAngle(img,11,13,15)
    #     cv2.putText(img, str(angle), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    # 每秒記錄一次身體位置
    frame_count += 1
    schedule.run_pending()

    # 跌倒判斷
    if len(lmList) != 0:
        fall_count = fall_detector.update(frame_count, lmList[9], lmList[0], lmList[23])

    cv2.putText(img, "fall_count:"+str(fall_count), (30, 100), cv2.FONT_HERSHEY_PLAIN, 2,(0, 0, 255), 3)
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break