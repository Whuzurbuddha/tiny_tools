import cv2
import os


def resize(cap, factor: float):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640 * factor)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480 * factor)


def set_camera_properties(cap):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, -12.0)
    cap.set(cv2.CAP_PROP_CONTRAST, 50.0)
    cap.set(cv2.CAP_PROP_SHARPNESS, 90.0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_AUTO_WB, 1)
    cap.set(cv2.CAP_PROP_EXPOSURE, 1200)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)


def main():
    default_cam = 2
    cap = cv2.VideoCapture(default_cam)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    set_camera_properties(cap)

    recording = False
    video_writer = None
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break
            
        image = cv2.rotate(frame, cv2.ROTATE_180)
        cv2.imshow('USB Camera', image)
        cv2.setWindowTitle('USB Camera', 'Microcam')
        factor = 1.0

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+'):
            factor += 0.5
            resize(cap, factor)
        elif key == ord('-'):
            resize(cap, factor)
        elif key == ord('s'):
            if not recording:
                screenshot_filename = '/home/alexander/Bilder/science/screenshot.jpeg'
                screenshot_dir = os.path.dirname(screenshot_filename)

                if not os.path.exists(screenshot_dir):
                    try:
                        os.makedirs(screenshot_dir)
                        print(f"Directory created: {screenshot_dir}")
                    except Exception as e:
                        print(f"Failed to create directory {screenshot_dir}: {e}")
                        continue

                if cv2.imwrite(screenshot_filename, frame):
                    print(f"Screenshot saved as {screenshot_filename}")
                    if os.path.exists(screenshot_filename):
                        print(f"File verified: {screenshot_filename}")
                    else:
                        print(f"File not found after saving: {screenshot_filename}")
                else:
                    print(f"Failed to save screenshot as {screenshot_filename}")
            else:
                print("Cannot take screenshot while recording.")

        elif key == ord('v'):
            if not recording:
                video_filename = '/home/alexander/Bilder/science/recording.avi'
                video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'DIVX'), 20,
                                               (frame_width, frame_height))
                recording = True
                print(f"Recording started: {video_filename}")
            else:
                print("Already recording.")

        elif key == ord('p'):
            if recording:
                video_writer.release()
                recording = False
                print("Recording stopped.")
            else:
                print("Not recording.")

        elif cv2.getWindowProperty('USB Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

        if recording:
            video_writer.write(frame)

    if recording:
        video_writer.release()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
