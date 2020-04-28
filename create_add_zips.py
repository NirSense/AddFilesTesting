#!/usr/bin/python
# Create duplicates of a zip file with an added prefix to all files. 
# Split the created zips so that they have no more than 200 files each
# By default add "1_" "2_" and "3_" to all files.

import argparse
import os
import glob
import shutil
import math

from zipfile import ZipFile

def MAX_ZIP_SIZE():
	return 200


def duplicate_zip(zip_path, n):
	
	temp_folder = create_temp_folder()
	with ZipFile(zip_path,'r') as submissions_zip:
		submissions_zip.extractall(temp_folder)

	for i in range(n):
		duplicate_zip_all_w_prefix(temp_folder, f"{i}_")

	shutil.rmtree(temp_folder)


def duplicate_zip_all_w_prefix(path, prefix):
	previous_wd = os.getcwd()
	os.chdir(path)
	prefixed_files = []
	for file in glob.glob("*"):
		prefixed_file = prefix+file #TODO due to instant feedback persistent files not having a file extension we won't be able to add the zip if we don't give them an extension, we'll just ignore it later
		shutil.copyfile(file, prefixed_file)
		prefixed_files.append(prefixed_file)

	to_zip = set()
	count = len(prefixed_files)
	for batch in range(math.ceil(count/MAX_ZIP_SIZE())): #run each batch
		batch_zip_path = os.path.join(previous_wd, f"{prefix}zip{batch}.zip")
		to_zip.clear()
		for i in range(batch*MAX_ZIP_SIZE() , min(count, MAX_ZIP_SIZE()*(batch+1) )): #inner index in 'skips' of 200
			to_zip.add(prefixed_files[i])
			zip_batch(to_zip, batch_zip_path) #Keep to zips of 200 or less
		#remove files from completed batch
		# cleanup and easy
		for file in to_zip:
			os.remove(file)

	os.chdir(previous_wd)

def zip_batch(files, zip_path):
	with ZipFile(zip_path, 'w') as batchfile:
		for file in files:
			batchfile.write(file)

def create_temp_folder():
	temp_path = "temp"
	while os.path.isdir(temp_path):
		temp_path+="p"
	os.makedirs(temp_path)
	
	return temp_path

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Create duplicates of given zip file with prefixes added to each file contained in it")
	parser.add_argument('zip_path', help="path to the zip to be duplicated")
	parser.add_argument('-n', help="number of copies to duplicate to", type=int, default=3)

	args = parser.parse_args()

	zip_path = args.zip_path
	n = args.n

	duplicate_zip(zip_path, n)