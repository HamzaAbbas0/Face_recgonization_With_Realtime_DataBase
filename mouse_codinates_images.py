import cv2

def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Mouse coordinates: ({x}, {y})")

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', POINTS)

frame = cv2.imread('Resources/background.png')
if frame is None:
    print("Error reading the image.")
    exit(1)

cv2.imshow('Image', frame)
while True:
    if cv2.waitKey(0) != -1 or cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
