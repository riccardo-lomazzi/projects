import os, json, sys, shutil
from pprint import pprint
from collections import defaultdict


def getJSONElement(data, ext):
	for el in data["paths"]:
		if (el["extension"] == ext):
			return el

def file_mover(json_path):
	JSONdata = json.load(json_path)
	fileList = defaultdict(list)
	countFiles = 0
	countFolders = 0
	with os.scandir() as dir: #for now, only scan current folder
		for entry in dir:
			if entry.is_dir():
				countFolders = countFolders + 1
				if(len(sys.argv) > 1 and sys.argv[1] == "-pd"):
					print(entry.name)
			if entry.is_file() and entry.name != os.path.basename(sys.argv[0]) and entry.name != os.path.basename(json_path.name):
				countFiles = countFiles + 1
				extension = os.path.splitext(entry.name)[1][1:]
				JSONelement = getJSONElement(JSONdata, extension)
				if(JSONelement is not None):
					fileList[JSONelement["path"]].append(entry.name) #add to file list

	print(str(countFolders) + " directories and " + str(countFiles) + " files found. This will be the directory structure after confirming changes: \n")
	for directory in fileList:
		print(directory)
		for f in fileList[directory]:
			print("-- " + f)
	answer = input("Confirm changes?: (type Y to proceed)")
	if answer == 'Y':
		for directory in fileList:
			for f in fileList[directory]:
				if not os.path.exists(directory):
					os.makedirs(directory)
				shutil.move(f, directory + "/" + f)
		print("Done")
	print("Program exit")


try:
	with open("paths.json") as paths:
		print("JSON File Found")
		file_mover(paths)
		
except IOError as error:
	print("json file with paths NOT found. Program can't continue without it")

