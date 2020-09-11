import os
import numpy as np
import pandas as pd

col_list = ['frame_timestamp', 'oid', 'x', 'y']

P_FILENAME = 'projection_matrix.txt'

class FileInformation:

	def __init__(self, filename, calibration_path):
		self.raw_data = pd.read_csv(filename, usecols=col_list)
		self.init_camera_calibration(calibration_path)

	def init_camera_calibration(self, calibration_path):

		if P_FILENAME in os.listdir():
			self.P = np.loadtxt(P_FILENAME)
		else:
			self.P = self.calculate_projection_matrix(calibration_path)

	def get_3D(self, pt):
		##0 PT = inv(self.P) * pt
		return pt[0], pt[1], 0

	def get_distance(self, pt1, pt2):

		x1, y1, z1 = self.get_3D(pt1)
		x2, y2, z2 = self.get_3D(pt2)

		return ((x1-x2)**2 + (y1-y2)**2)**0.5

	def get_info(self):

		crown_data = self.raw_data[self.raw_data.oid == 1]

		crown_x, crown_y = crown_data['x'].tolist(), crown_data['y'].tolist()
		timestamps = crown_data['frame_timestamp'].tolist()

		total_distance = 0
		speed = [0]

		for i in range(len(crown_x) - 1):
			distance = self.get_distance((crown_x[i], crown_y[i]), (crown_x[i+1], crown_y[i+1]) )
			speed.append(distance / (timestamps[i+1] - timestamps[i]))
			total_distance += distance

		avg_speed = sum(speed)/len(speed)

		return {
				"total_distance": round(total_distance, 2),
				"average_speed": round(avg_speed, 2)
		}

	def calculate_projection_matrix(self, calibration_path):
		matches = np.loadtxt(calibration_path)
		P = self.camera_calibration(matches[:,0:2], matches[:,2:])
		np.savetxt(P_FILENAME, P)
		return P

	@staticmethod
	def camera_calibration(pts2d, pts3d):
		assert len(pts2d) == len(pts3d)
		
		num_data = len(pts2d)
		
		## Build matrix A for Ap = 0
		A = np.zeros((2*num_data, 12))
		for i in range(num_data):
			[x, y] = pts2d[i]
			[X, Y, Z] = pts3d[i]
			V = np.array([X, Y, Z, 1])
			A[2*i, 4:8] = V
			A[2*i, 8:12] = -y*V
			A[2*i+1, 0:4] = V
			A[2*i+1, 8:12] = -x*V

		## Do SVD of A to solve Ap = 0
		U, S, V = np.linalg.svd(A)
		P = V[-1].reshape(3,4)

		return P
