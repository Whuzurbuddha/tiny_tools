import cv2


def set_camera_properties(cap, brightness=0.5, sharpness=0.5):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cap.set(cv2.CAP_PROP_CONTRAST, sharpness)


def main():
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    set_camera_properties(cap, brightness=0.5, sharpness=0.5)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow('USB Camera', frame)
        cv2.setWindowTitle("USB Camera", "Microcam")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_filename = filepath
            cv2.imwrite(screenshot_filename, frame)
            print(f"Screenshot saved as {screenshot_filename}")
        elif cv2.getWindowProperty('USB Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
