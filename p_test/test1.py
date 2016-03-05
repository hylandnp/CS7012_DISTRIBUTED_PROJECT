import pysnmp
import os

def gci(path):
	file_paths = []
	if os.path.isdir(path):
		pass
	else:
		file_paths.append(path)
		return file_paths
	try:
		parents = os.listdir(path)
		for parent in parents:
			child = os.path.join(path, parent)
			# print child
			if os.path.isdir(child):
				file_paths = file_paths + gci(child)
			else:
				file_paths.append(child)
		return file_paths
	except Error:
		print "error in file_search\n"
files = gci('/etc')
print files