'''
This script cleans up a directory or multiple directories and properly sorts out files in the given directory based of the filetype.
Eg: All image file are moved to an existing or newly created "Pictures" folder, video files to the "Videos" folder, audio files to the "Audios" folder, etc.
'''
import os, sys
import json, re
import time


swd, *directories = sys.argv
existing_directories = {}

extensions = {}
with open(os.path.join(os.path.dirname(swd), 'formats.json')) as file_formats:
	file_formats = json.load(file_formats)
	for fmt in file_formats:
		extensions.update({ext: fmt for ext in file_formats[fmt]})


'''
# intended for segmenting documents into subfolders for each filetype
def get_extension(file):
	basename = os.path.basename(file)
	return basename.rsplit('.', 1)[-1]
'''
def check_folder_existence(dirname, *basenames):
	for name in basenames:
		dir_ = os.path.join(dirname, name)
		if os.path.exists(dir_):
			return name.title(), dir_
	return None

def create_folder(where, name):
	directory = os.path.join(where, name)
	if not os.path.exists(directory):
		os.mkdir(directory)
	return directory

def move_file(file, folder):
	if '/' in folder:
		folder = os.path.basename(folder)
	os.rename(
		file,
		os.path.join(
			os.path.dirname(file),
			folder,
			os.path.basename(file)
		)
	)

def get_file_type(file):
	file_ext = re.search(r'(?<=.)\.\w+$', file).group().lower()
	try:
		type_ = extensions[file_ext] + 's'
	except KeyError:
		type_ = 'Documents'
	finally:
		return type_

def clean(directory, file):
	if os.path.isdir(os.path.join(directory, file)):
			existing_directories[file.title()] = 0
	else:
		# identify file type
		filetype = get_file_type(file)
		# find out if a folder already exists for the given file
		existence = check_folder_existence(
			filetype, filetype.lower(), filetype.upper()
		)
		if existence:
			name, dir_ = existence
		else:
			name, dir_ = filetype, create_folder(directory, filetype.title())
		# save the folder path
		if name not in existing_directories:
			existing_directories[name] = dir_
		# move file to its respective folder
		print(f'Moving {file!r} to {os.path.basename(existing_directories[name])}...')
		move_file(
			os.path.join(directory, file),
			existing_directories[name]
		)

def scan_and_clean(directory):
	# check files in given directory
	files_to_clean = os.listdir(directory)

	for file in files_to_clean:
		clean(directory, file)
		time.sleep(.1)


if __name__ == "__main__":
	for dir_ in directories:
		scan_and_clean(dir_)
		existing_directories = {}

	del directories, existing_directories
