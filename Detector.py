import cv2 
import numpy as np 

# Read image. 
img = cv2.imread('lots.jpg', cv2.IMREAD_COLOR) 

# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

num_pennies = 0

num_dimes = 0

num_quarters = 0

num_nickels = 0

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
		if r < 110 and r > 90:
			num_pennies += 1
		if r > 70 and r < 80:
			num_dimes += 1
		# Draw the circumference of the circle. 
		cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
	
	total_money = (num_dimes * 10 + num_pennies + num_nickels * 5 + num_quarters * 25) / 100
	cv2.putText(img, "Total dollars: " + str(total_money), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	cv2.putText(img, "Number of coins: " + str(len(detected_circles[0])), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	cv2.imshow("Detected Circle", img) 
	cv2.waitKey(0) 