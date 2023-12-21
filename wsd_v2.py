import cv2
import numpy as np

# Function to calculate the exponential moving average of a value
def exponential_moving_average(current, previous, alpha):
    return alpha * current + (1 - alpha) * previous

def main():
    # Open the default camera (usually the built-in webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Parameters for smoothing
    alpha = 0.2  # Smoothing factor
    consecutive_frames = 5  # Number of consecutive frames for stabilization

    # Variables to store previous position
    prev_x, prev_y = 0, 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Example: Detect edges using Canny
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)  # You can adjust the thresholds

        # Find contours in the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area to find the square
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 5000:  # Adjust the area threshold as needed
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) == 4:
                    # Draw a bounding box around the square
                    x, y, w, h = cv2.boundingRect(approx)

                    # Smoothing using exponential moving average
                    x = int(exponential_moving_average(x, prev_x, alpha))
                    y = int(exponential_moving_average(y, prev_y, alpha))

                    thickness = 5  # Adjust the thickness as needed
                    color = (0, 255, 0)  # Green color in BGR
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

                    # Update previous positions
                    prev_x, prev_y = x, y

                    # Reset the consecutive frame counter
                    consecutive_frames = 5

        # If no square is detected, use the previous position
        if consecutive_frames > 0:
            x, y = prev_x, prev_y
            consecutive_frames -= 1

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
