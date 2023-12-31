import cv2
import numpy as np

# # Function to calculate the moving average of a list of points
# def moving_average(points, n=5):
#     return np.convolve(points, np.ones(n)/n, mode='valid')

def main():
    # Open the default camera (usually the built-in webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # List to store the previous positions of the bounding boxes
    prev_bounding_boxes = []

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Example: Detect edges using Canny
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and improve edge detection
        # blur = cv2.GaussianBlur(gray, (3, 3), 0)

        blur = cv2.GaussianBlur(gray, (13, 13), 0)
        # blur = gray
        sigma = np.std(blur)
        mean = np.mean(blur)
        lower = int(max(0, (mean - sigma)))
        upper = int(min(255, (mean + sigma)))

        edges = cv2.Canny(blur, lower, upper)  # You can adjust the thresholds

        # Find contours in the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area to find the square
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Adjust the area threshold as needed
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) == 4:
                    # Draw a thicker bounding box around the square
                    x, y, w, h = cv2.boundingRect(approx)

                    # # Smoothing using moving average
                    # if len(prev_bounding_boxes) > 10:
                    #     x = int(moving_average([x, prev_bounding_boxes[-1][0]], n=3)[0])
                    #     y = int(moving_average([y, prev_bounding_boxes[-1][1]], n=3)[0])

                    thickness = 5  # Adjust the thickness as needed
                    color = (0, 255, 0)  # Green color in BGR
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

                    # # Update the list of previous bounding boxes
                    # prev_bounding_boxes.append((x, y))

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
