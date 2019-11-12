import numpy as np  
import cv2 
import matplotlib.image as mpimg
from matplotlib import pyplot as plt 
from open3d import *
from scipy import signal
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type = str, required=True, help="the path to the input image")
ap.add_argument("-d", "--distort", type = int, required=True, help="1 means distort the image point cloud")
args = vars(ap.parse_args())
path_image = args["image"]
distort = args["distort"]

#Preprocess the image, resize, add noise if required
img = mpimg.imread(path_image)
img = cv2.resize(img,(256,256))
l , w, c  = img.shape
print(l,w,c)

""" add noise
mu =  np.max(img) / 25
print("mu is :", mu)
noise = np.random.normal(0,mu,img.shape)
img = noise + img
"""

def distort_pcd(my_img_position, **kwargs):
	l = my_img_position.shape[0] 
	t = np.linspace(0,1,l,endpoint = False)
	#sig = 0.05 * np.sin(8*np.pi*t)	
	#sig = np.sinh(sig)
	sig = np.sin(0.8*np.pi*t)	
	#t = np.linspace(-0.5,0.5,l,endpoint = False)
	#sig = 0.1 * np.sinc(8*np.pi*t)
	my_img_position[:,2] = sig
	return my_img_position

def convert_imgTo_pcd(img, **kwargs):
	f = kwargs.get('f',None)
	intensity_f_r = np.reshape(img[:,:,0],(l*w,1))
	intensity_f_g = np.reshape(img[:,:,1],(l*w,1))
	intensity_f_b = np.reshape(img[:,:,2],(l*w,1))
	x = np.arange(0,w,1)
	y = np.arange(l,0,-1)
	mesh_x, mesh_y = np.meshgrid(x,y)
	x_f = np.reshape(mesh_x,(l*l,1))
	y_f = np.reshape(mesh_y,(l*l,1))
	z_f = np.zeros((l*l,1))
	my_img_position = np.concatenate((x_f,y_f,z_f),axis=1)
	my_img_position = my_img_position/l
	
	if distort == 1:
	     my_img_position = distort_pcd(my_img_position)
	
	my_img_color = np.concatenate((intensity_f_r,intensity_f_g,intensity_f_b),axis=1)
	my_img_color = ((my_img_color - my_img_color.min()) / (my_img_color.max() - my_img_color.min()))
	pcd = PointCloud()
	pcd.points = Vector3dVector(my_img_position)
	pcd.colors = Vector3dVector(my_img_color)
	write_point_cloud("image_pcd.ply", pcd)
	pcd_load = read_point_cloud("image_pcd.ply")
	draw_geometries([pcd_load])
	return my_img_position, my_img_color

my_img_position,  my_img_color = convert_imgTo_pcd(img)
np.savez('position.npz', position=my_img_position)
np.savez('texture.npz', texture=my_img_color)
