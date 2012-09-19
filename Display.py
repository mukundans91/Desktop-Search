def R(doc):
	for fields in doc:
		print fields[0]," : ",fields[1]
		print 

def Display(results,screenWidth):
	i=1
	for result in results:
		print "(",i,")",
		i+=1
		R(result.items())
		print '-'*screenWidth
