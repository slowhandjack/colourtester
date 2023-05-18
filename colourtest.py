import cv2
import numpy as np
import os
import time

# Display a white image to act as a basic flash
screen_width, screen_height = 2880, 1800  # ( Todo: Find a way to automatically adjust to screen resolution)
white_image = np.ones((screen_height, screen_width, 3), dtype=np.uint8) * 255
cv2.namedWindow("Fullscreen", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Fullscreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("Fullscreen", white_image)
cv2.waitKey(1) 

def take_picture():
    # Open the webcam
    capture = cv2.VideoCapture(0)
    time.sleep(2) # Janky way to prolong the shutter speed (for increased exposure) on the built-in webcam
    # Read a frame from the webcam
    ret, frame = capture.read()

    # Release the webcam
    capture.release()

    return frame

def save_picture(frame, output_path):
    # Save the frame as an image file
    cv2.imwrite(output_path, frame)

    print(f"Picture saved: {output_path}")

def analyze_dominant_colour(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV colour space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the colour ranges
    colour_ranges = {
    'Red': ([0, 120, 70], [10, 255, 255]),
    'Orange': ([11, 120, 70], [20, 255, 255]),
    'Yellow': ([21, 120, 70], [30, 255, 255]),
    'Green': ([36, 120, 70], [70, 255, 255]),
    'Blue': ([90, 120, 70], [130, 255, 255]),
    'Purple': ([131, 120, 70], [160, 255, 255]),
    'Pink': ([161, 120, 70], [179, 255, 255]),
    }

    # Create masks for the defined colour ranges
    masks = {}
    for colour, (lower_range, upper_range) in colour_ranges.items():
        mask = cv2.inRange(hsv_image, np.array(lower_range), np.array(upper_range))
        masks[colour] = mask

    # Identify the dominant colour
    dominant_colour = max(masks, key=lambda x: cv2.countNonZero(masks[x]))

    return dominant_colour

def main():
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output file path
    output_file = os.path.join(script_dir, "captured_picture.jpg")

    # Take a picture
    frame = take_picture()

    # Save the picture
    save_picture(frame, output_file)

    # Analyze the dominant colour in the captured picture
    dominant_colour = analyze_dominant_colour(output_file)

    print('The dominant colour in the image is:', dominant_colour)

if __name__ == "__main__":
    main()