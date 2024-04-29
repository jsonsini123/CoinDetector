import cv2 
import numpy as np 

# Read image. 
img = cv2.imread('lots.jpg', cv2.IMREAD_COLOR) 

# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray,
                           cv2.HOUGH_GRADIENT,
                           minDist=70,
                           dp=1.1,
                           param1=150,
                           param2=95,
                           minRadius=6,
                           maxRadius=150)

# Draw circles that are detected. 
if detected_circles is not None: 

	# Convert the circle parameters a, b and r to integers. 
	detected_circles = np.uint16(np.around(detected_circles)) 
	print(len(detected_circles))

	for pt in detected_circles[0, :]: 
		a, b, r = pt[0], pt[1], pt[2] 

		# Draw the circumference of the circle. 
		cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
		
	cv2.putText(img, "Number coins: " + str(len(detected_circles[0])), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	cv2.imshow("Detected Circle", img) 
	cv2.waitKey(0) 
