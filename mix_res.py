#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
import hashlib
import xml.etree.ElementTree as ET


DIR = sys.path[0];
dest_dir = DIR + '/res_mapping/'

def parsePlist(path, name):
	print "parsePlist = ", path, name
	path = os.path.abspath(path)
	tree = ET.parse(path);
	root = tree.getroot()
	totalDict = root.find('dict')
	flag = False;
	i = 0
	for oneElement in totalDict:
		if oneElement.tag == 'key' and oneElement.text == 'metadata':
			flag = True
			j = 0;
			for key in totalDict[i+1]:
				if key.tag == 'key' and key.text == 'textureFileName':
					totalDict[i+1][j+1].text = str(name);
					break;
				j += 1
			break
		i += 1
	tree.write(path)

def func(arg, dirname, names):
	for name in names:
		if os.path.splitext(name)[1] == '.png' or os.path.splitext(name)[1] == '.plist':
			
			dest = dest_dir
			index = dirname.find('/res')
			file2 = dirname[index:]
			file2 = file2[1:]
			file2 = os.path.join(file2, name)
			mdfive = hashlib.md5()
			mdfive.update(str(file2))
			md5_value = mdfive.hexdigest()
			level1 = md5_value[0:2]
			level2 = md5_value[2:]
			dest = os.path.join(dest, level1)

			if not os.path.exists(dest):
				os.mkdir(dest)
			# shutil.copy(os.path.join(dirname, name), dest)
			# os.chdir(os.path.abspath(dest))
			print "dir = ", dirname, name, file2
			shutil.move(os.path.join(dirname, name), os.path.join(dest, level2))
			os.chdir(DIR)
			arg[str(file2)] = md5_value

if __name__ == "__main__":
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
	os.mkdir(dest_dir)
	if os.path.exists(os.path.join(DIR, 'res')):
		shutil.rmtree(os.path.join(DIR, 'res'))
	shutil.copytree(os.path.join(DIR, 'back'), os.path.join(DIR, 'res'))

	mapping = {}
	os.path.walk(os.path.join(DIR, 'res'), func, mapping)

	for key in mapping.keys():
		res_name = key
		ext = res_name[-6:]
		if ext == '.plist':
			name = res_name[0:-6]
			name = name + ".png"
			if mapping[name]:
				png_hash = mapping[name]
				png_hash_dir = png_hash[0:2]
				png_hash_name = png_hash[2:]

				plist_hash = mapping[res_name]
				plist_hash_dir = plist_hash[0:2]
				plist_hash_name = plist_hash[2:]
				plist_path = os.path.join(dest_dir, plist_hash_dir, plist_hash_name)

				mapping[name] = plist_hash_dir + png_hash_name

				png_source_path = os.path.join(dest_dir, png_hash_dir, png_hash_name)
				png_dest_path = os.path.join(dest_dir, plist_hash_dir, png_hash_name)
				shutil.move(png_source_path, png_dest_path)
				parsePlist(plist_path, png_hash_name)

	if not os.path.exists(os.path.join(DIR, "src")):
		os.mkdir(os.path.join(DIR, "src"))

	js = open(os.path.join(DIR, 'src', 'mapping.js'), 'w+')
	js.write("var res_mapping = {\n")
	for key in mapping.keys():
		js.write("'")
		js.write(key)
		js.write("' : '")
		js.write(mapping[key])
		js.write("',\n")
	js.write("}")
	js.close()

	shutil.rmtree(os.path.join(DIR, "res"))
	shutil.move(dest_dir, os.path.join(DIR, "res"))
