import glob,os
def getFilePathsByType(root,typeoffile):
	"""Generator function for the files of type 'typeoffile' under the directory 'root'"""
	filepaths=[]
	filetype=typeoffile.lower()
	if os.path.exists(root):
		for root,unused,un in os.walk(root):
			for fil in glob.glob(root+"/*."+filetype):
				yield fil,filetype

def getFileContent(f,t):
	"""Based on type 't' the file 'f' is opened by the corresponding script and the content is returned as a string"""
	import subprocess
	content=""
	err=""
	try:
		if t=="txt":
			process=subprocess.Popen("cat "+f,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			content,err=process.communicate()
		elif t=="pdf":
			process=subprocess.Popen("pdftotext -q '"+f+"' -",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			content,err=process.communicate()
	except:
		pass
	return content,err

if __name__=="__main__":
	print getFilePathsByType.__doc__
	f=getFilePathsByType("/home","PDF")
	i=4
	for fname,typ in f:
		print fname+"\tTYPE:",typ
		if i==0:
			print getFileContent(fname,typ)
			i+=1
#Use less pager for better view in __main__
