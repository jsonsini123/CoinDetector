import cv2 
import numpy as np 
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

class Scan:
	def __init__(self):
		self.num_pennies = 0

		self.num_dimes = 0

		self.num_quarters = 0

		self.num_nickels = 0

		# Create video
		self.video = cv2.VideoCapture(0)

	def evaluate(self, image):
		# Convert to grayscale. 
		self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

		# Blur using 3 * 3 kernel. 
		self.gray_blurred = cv2.blur(self.gray, (3, 3)) 

		# Apply Hough transform on the blurred image. 
		detected_circles = cv2.HoughCircles(self.gray,
								cv2.HOUGH_GRADIENT,
								minDist=90,
								dp=1.1,
								param1=150,
								param2=95,
								minRadius=45,
								maxRadius=130)

		# Draw circles that are detected. 
		if detected_circles is not None: 

			# Convert the circle parameters a, b and r to integers. 
			detected_circles = np.uint16(np.around(detected_circles)) 
			print(len(detected_circles))

			for pt in detected_circles[0, :]: 
				a, b, r = pt[0], pt[1], pt[2] 
				if r < 96 and r > 84:
					self.num_pennies += 1
				if r > 65 and r < 84:
					self.num_dimes += 1
				if r > 95 and r < 103:
					self.num_nickels += 1
				if r > 103:
					self.num_quarters += 1
				# Draw the circumference of the circle. 
				cv2.circle(image, (a, b), r, (0, 255, 0), 2) 
			
			total_money = (self.num_dimes * 10 + self.num_pennies + self.num_nickels * 5 + self.num_quarters * 25) / 100
			cv2.putText(image, "Total dollars: " + str(total_money), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.putText(image, "Number of coins: " + str(len(detected_circles[0])), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.imshow("Detected Circle", image) 
			cv2.waitKey(0) 
		else:
			cv2.putText(image, "No Coins Detected", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 2)
			cv2.imshow("Detected Circle", image) 
			cv2.waitKey(0) 


	def run(self):
		frame = None
		while self.video.isOpened():
			# Get the current frame
			frame = self.video.read()[1]

			# Convert it to an RGB image
			image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			#Guides
			cv2.putText(image, "Place Penny in Green Circle to Scale. Press 'q' to evaluate image", (400,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.circle(image, (950, 650), 94, (0, 255, 0), 2)

			# Change the color of the frame back
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			cv2.imshow('test', image)

			key = cv2.waitKey(50) & 0xFF
	
			# Break the loop if the user presses 'q'
			if key == ord('q'):
				break


		self.video.release()
		cv2.destroyAllWindows()
		# Flip image back
		return(frame)

if __name__ == "__main__":        
	g = Scan()
	img = g.run()
	# cv2.imshow("Image", img)
	# cv2.waitKey(0)
	g.evaluate(img)

