import cv2
import numpy as np

# Load the image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Apply the Sobel filter for horizontal and vertical edges
sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# Combine the horizontal and vertical edges using magnitude and direction
mag, angle = cv2.cartToPolar(sobelx, sobely, angleInDegrees=True)
