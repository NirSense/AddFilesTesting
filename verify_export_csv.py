#!/usr/bin/python
# Test CSV for validity of add files

import csv
import argparse

def read_export_csv(csv_path):
	group_dict = {}
	with open(csv_path, 'r') as group_csv:
		reader = csv.DictReader(group_csv)
		for row in reader:
			group_dict[row["File name"]] = row["Group"]
	return group_dict

def verify_added_prefix(before_dict, after_dict, prefix):
	ret = True
	for k, v in before_dict.items():
		after_name = prefix+k#TODO
		is_there = after_name in after_dict
		same_group = is_there and after_dict[after_name] == v
		if not is_there:
			print(f"Error: Missing prefix {prefix} for file name: {k}")
			ret = False
		elif not same_group:
			print(f"Error: Mismatched group for file: {k} with prefix {prefix}; initial classification: {v}, after: {after_dict[after_name]}")
			ret = False
	return ret

def verify_csvs(after_csv_path, before_csv_path, n):
	before_group_dict = read_export_csv(before_csv_path)
	after_group_dict = read_export_csv(after_csv_path)

	verified = True

	for i in range(n):
		verified = verify_added_prefix(before_group_dict, after_group_dict, f"{i}_") and verified

	print("Passed" if verified else "Failed")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Test before and after export .csv files for added files being in the model")
	parser.add_argument('-a', help="path to the export CSV from AFTER adding the files to the model", required=True)
	parser.add_argument('-b', help="path to the export CSV from BEFORE adding the files to the model", required=True)
	parser.add_argument('-n', help="number of file duplications to look for", default=3)

	args = parser.parse_args()

	# after_csv_path = args.a
	# before_csv_path = args.b

	verify_csvs(args.a, args.b, args.n)

