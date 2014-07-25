import sys
import os
import hashlib
from PIL import Image


def hash_function(last_hash, in_data):
	return int(hashlib.md5(str(last_hash) + str(in_data)).hexdigest(), 16)
	#return in_data * 1001230123231230123312L % 21201231233L


def scramble(image_in):
	in_list = list(image_in)
	in_list_len = len(in_list)
	tmp = dict()
	print len(in_list)
	last_hash=0
	for i in range(0, in_list_len):
		#find where to put i-th pixel
		act_hash = hash_function(last_hash, i)
		j = act_hash % in_list_len
		last_hash = act_hash
		if i % 10000 == 0:
			print i
		while(tmp.get(j) is not None):
			j = (j + 1) % in_list_len
		tmp[j] = in_list[i]
	out_list = list()
	for i in range(0, in_list_len):
		out_list.append(tmp[i])
	return out_list


def descramble(image_in):
	in_list = list(image_in)
	in_list_len = len(in_list)
	tmp = dict()
	out_list = dict()
	print len(in_list)
	last_hash=0
	for i in range(0, in_list_len):
		#find where to put i-th pixel
		act_hash = hash_function(last_hash, i)
		j = act_hash % in_list_len
		last_hash = act_hash
		if i % 10000 == 0:
			print i
		while(tmp.get(j) is not None):
			j = (j + 1) % in_list_len
		tmp[j] = 1
		out_list[i] = in_list[j]
	out_list2 = list()
	for i in range(0, in_list_len):
		out_list2.append(out_list[i])
	return out_list2


def main():
	print "hello"
	im = Image.open(sys.argv[1], "r")
	print im.size
	#im.show()
	im2 = Image.new(im.mode, im.size)
	im3 = Image.new(im.mode, im.size)
	image_data = im.getdata()

	image_data_2 = scramble(list(image_data))

	im2.putdata(image_data_2)
	im2.show()

	image_data_3 = descramble(list(image_data_2))
	im3.putdata(image_data_3)
	im3.show()
	


if __name__=="__main__":
	main()

