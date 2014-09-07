import sys
import os
import hashlib
import bisect
from PIL import Image

def point_mapping(hash_fun, image_len, hash_init_val):
	unused_points = range(image_len)
	last_hash = hash_init_val
	for i in range(image_len):
		act_hash = hash_fun(last_hash, i)
		last_hash = act_hash
		j = act_hash % image_len
		p = bisect.bisect_left(unused_points, j)
		if p == len(unused_points): #there is no unused point to the end,
			p = bisect.bisect_left(unused_points, 0) #search from the start
		map_point = unused_points.pop(p)
		yield map_point

def hash_point(last_hash, in_point):
	return int(hashlib.md5(str(last_hash) + str(in_point)).hexdigest(), 16)
	#return in_point * 1001230123231230123312L % 21201231233L
	#return in_point * 200

def process_key(key_in):
	dark_points = list() #list of indices of dark points
	light_points = list() #list of indices of light points
	for i in range(len(key_in)):
		if sum(key_in[i]) > 384:
			light_points.append(i)
		else:
			dark_points.append(i)
	return (light_points, dark_points)

def scramble(image_in, key_in, hash_init_light, hash_init_dark, descramble=False):
	in_len = len(image_in)
	image_out = list(image_in)
	(lp, dp) = process_key(key_in)
	i = 0
	#first map the upper half of the image to the light points of the key image
	for m in point_mapping(hash_point, len(lp), hash_init_light):
		if not descramble:
			image_out[lp[m]] = image_in[i]
		else:
			image_out[i] = image_in[lp[m]]
		i += 1
	#then the lower half to the dark points of the key image
	for m in point_mapping(hash_point, len(dp), hash_init_dark):
		if not descramble:
			image_out[dp[m]] = image_in[i]
		else:
			image_out[i] = image_in[dp[m]]
		i += 1
	return image_out

def main():
	if (3 != len(sys.argv)):
		print "Usage: " + sys.argv[0] + " image key"
		exit(0)
	im_filename = sys.argv[1]
	key_filename = sys.argv[2]
	im = Image.open(im_filename, "r")
	image_data = im.getdata()
	key = Image.open(key_filename, "r")
	key_data = key.getdata()

	image_data_2 = scramble(image_data, key_data, 0, 10)
	im2 = Image.new(im.mode, im.size)
	im2.putdata(image_data_2)
	im2.show()

	image_data_3 = scramble(image_data_2, key_data, 0, 10, True)
	im3 = Image.new(im.mode, im.size)
	im3.putdata(image_data_3)
	im3.show()
	
if __name__=="__main__":
	main()

