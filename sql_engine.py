import sys
import csv
import sqlparse

## Command line Agruments check ##
if len(sys.argv) !=2:
	print 'Incorrect arguments given!'
	print 'usage: python sql_engine.py <sql_query>'
	sys.exit(0)

### Reading table headers from metadata.txt ###
try:
	File = open("metadata.txt")
except IOError:
	print 'NO metadata found!!'
else:	
	tableList= File.readlines()
	tableList.pop()
	for i, item in enumerate(tableList):
		item=item.replace("\n","")
		tableList[i]=item
	i=0
	tables=[]								# list of lists for storing table headers
	for j in range(len(tableList)):
	    if tableList[j]=="<begin_table>":
	        i=j
	    if tableList[j]=="<end_table>":    
	        tables.append(tableList[i+1:j])	
	File.close()
print tables       

### Reading data from all csv files ###
tableData={}							# dict of tableName:Data
tableTemp=[] 
for i in tables:
	try:
		File = open(i[0]+'.csv')
	except IOError:
		print i[0]+'.csv' + ' does not exist!!'
	else:	
		reader = csv.reader(File)
		tableTemp = list(reader)
		tableData[i[0]]=tableTemp
		File.close()
print tableData	
