import cv2


def run_camera():
    # Open the default camera (usually the built-in webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Example: Draw a bounding box
        x, y, w, h = 100, 100, 200, 200  # Bounding box coordinates (change as needed)
        color = (0, 255, 0)  # Green color in BGR
        thickness = 2  # Thickness of the bounding box

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

