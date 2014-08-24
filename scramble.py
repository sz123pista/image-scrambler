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

def scramble(image_in, hash_init_val, descramble=False):
	in_len = len(image_in)
	image_out = list(image_in)
	i = 0
	for m in point_mapping(hash_point, in_len, hash_init_val):
		if not descramble:
			image_out[m] = image_in[i]
		else:
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

	image_data_2 = scramble(list(image_data), 0)

	im2.putdata(image_data_2)
	im2.show()

	image_data_3 = scramble(list(image_data_2), 0, True)
	im3.putdata(image_data_3)
	im3.show()
	


if __name__=="__main__":
	main()

