from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import QueryParser

import sys,os,subprocess
import File
import Display


import sys,fcntl,termios,struct
data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234')
h,w=struct.unpack('hh',data)
percentSize=14
screenWidth=w
def updateIndex(ix,path,w=140,percentSize=10):
	writer=ix.writer()
	total=0
	for types in ("TXT","PDF"):
		process=subprocess.Popen("ls -R '"+path+"' | grep '."+types.lower()+"' | wc -l",shell=True,stdout=subprocess.PIPE)
		total,err=process.communicate()
		total=int(total)
		print total," files"
#		break
		counter=0
		print "Indexing "+types+" files:"
		for fname,typ in File.getFilePathsByType(path,types):
			rest=w-(len('Indexing '+fname)%w)
			rest=rest-percentSize
			print 'Indexing '+fname,
			print "."*rest,
			print "[ %3s%% ]"%(str(int(counter*1.0/total*1.0*100)))
			try:
				content,err=File.getFileContent(fname,typ)
				content=content.decode("utf-8",'replace')
				writer.add_document(title=unicode(fname.split('/')[-1]),path=unicode(fname),
					content=content,Type=unicode(typ))
				if err:
					print "Error indexing "+fname+"\n"+err
				err=""
			except UnicodeDecodeError:
				print 'The File '+fname+" cannot be indexed"
			counter+=1

	writer.commit()
if len(sys.argv)==1:
	try:
		if not os.path.exists("index"):
			os.mkdir("index")
		
			schema=Schema(title=TEXT(stored=True),content=TEXT,path=ID(stored=True),Type=ID(stored=True))	
			#stored=True indicates the text is indexed as well as retured when queried
	
			ix=create_in("index",schema)
			updateIndex(ix,"/home",w,percentSize)
		else:
			ix=open_dir("index")
			queryString='1'
			while True:
				queryString=raw_input('Enter Query : ')
				if queryString=="end!":
					break
				#queryString,typ=File.strsplit(queryString)
				with ix.searcher() as searcher:
					parser=QueryParser("content",ix.schema)
					query=parser.parse(unicode(queryString))
					results=searcher.search(query)
					Display.Display(results,screenWidth)
	except KeyboardInterrupt:
		pass
else:
	if "update" in sys.argv:
		try:
			ix=open_dir("index")
			updateIndex(ix,"/media",w,percentSize)
		except:
			pass
