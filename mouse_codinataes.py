import cv2

def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Mouse coordinates: ({x}, {y})")

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', POINTS)

cap = cv2.VideoCapture('Videos/mumbaitraffic.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    if cv2.waitKey(0) & 0xFF == 27 or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
