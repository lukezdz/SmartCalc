import shutil, random, os

dirpath = '.\\Dataset\\Train'
destpath = '.\\Dataset\\Test'

# put all folder names here:
folders = []

for folder in folders:
	files = random.sample(os.listdir(dirpath + '\\' + folder), 100)
	for file in files:
		srcpath = os.path.join(dirpath + '\\' + folder, file)
		
		pathToDestFolder = destpath + '\\' + folder
		if not os.path.exists(pathToDestFolder):
			os.makedirs(pathToDestFolder)

		shutil.copy(srcpath, pathToDestFolder)
		os.remove(srcpath)