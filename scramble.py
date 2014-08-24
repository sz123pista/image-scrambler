import sys
import os
import hashlib
from PIL import Image


def point_mapping(hash_fun, image_len, hash_init_val):
	used_points = list() #TODO: improve this!
	last_hash = hash_init_val
	for i in range(image_len):
		act_hash = hash_fun(last_hash, i)
		last_hash = act_hash
		map_point = act_hash % image_len
		while map_point in used_points:
			map_point = (map_point + 1) % image_len
		used_points.append(map_point)
		yield map_point

def hash_point(last_hash, in_point):
	return int(hashlib.md5(str(last_hash) + str(in_point)).hexdigest(), 16)
	#return in_point * 1001230123231230123312L % 21201231233L

def scramble(image_in):
	in_list_len = len(image_in)
	image_out = list(image_in)
	i = 0
	for m in point_mapping(hash_point, in_list_len, 0):
		image_out[m] = image_in[i]
		i += 1
	return image_out

def descramble(image_in):
	in_list_len = len(image_in)
	image_out = list(image_in)
	i = 0
	for m in point_mapping(hash_point, in_list_len, 0):
		image_out[i] = image_in[m]
		i += 1
	return image_out

def main():
	print "hello"
	im = Image.open(sys.argv[1], "r")
	print im.size
	#im.show()
	im2 = Image.new(im.mode, im.size)
	im3 = Image.new(im.mode, im.size)
	image_data = im.getdata()

	image_data_2 = scramble(list(image_data)[:1000])

	im2.putdata(image_data_2)
	im2.show()

	image_data_3 = descramble(list(image_data_2))
	im3.putdata(image_data_3)
	im3.show()
	


if __name__=="__main__":
	main()

