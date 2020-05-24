import shutil, random, os

dirpath = '.\\Dataset\\Train'
destpath = '.\\Dataset\\Test'

folders = ['(', ')']

for folder in folders:
	files = random.sample(os.listdir(dirpath + '\\' + folder), 100)
	for file in files:
		srcpath = os.path.join(dirpath + '\\' + folder, file)
		shutil.copy(srcpath, destpath + '\\' + folder)
		os.remove(srcpath)