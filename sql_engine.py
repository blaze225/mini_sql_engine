import sys
from sys import stdout
import csv
import sqlparse

def printAllCols(tabs,tables,tableDataR):	
	""" Printing all columns for multiple tables """
	tabs=tabs.replace(' ','')
	tabsList=tabs.split(',')
	print tabsList
	for tab in tabsList:
		print ' '.join(tables[tab]),
	stdout.write("\n")	 
	for tab in tabsList:
		for i in tableDataR[tab]:
			print ' '.join(i)

def getColIndices(cols,tables,tabName):
	""" Get indices of columns in cols in a list"""
	cols=cols.replace(' ','')
	colList=cols.split(',')
	colIndices=[]
	for i in colList:
		colIndices.append(tables[tabName].index(i))
	return colIndices		

def printCols(cols,tabs,tables,tableDataR):
	""" Print multiple columns from a table """
	tabs=tabs.replace(' ','')			# 1 table
	cols=cols.replace(' ','')
	#tabsList=tabs.split(',')
	colList=cols.split(',')
	colNums=getColIndices(cols,tables,tabs)
	for i in range(len(tables[tabs])):			# table attribute names 
		if i in colNums:
			print tables[tabs][i],
	stdout.write("\n")		
	for i in range(len(tableDataR[tabs])):		# rows
	 	for j in range(len(tableDataR[tabs][i])):
	 		if j in colNums:
	 			print tableDataR[tabs][i][j],
		stdout.write("\n")			

def convertRowsToCols(tableTemp):
	lst = []
	for i in tableTemp[0]:
		lst.append([])
	for row in tableTemp:
		for i in range(len(row)):
			lst[i].append(row[i])
	return lst		

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
	sys.exit(0)
else:	
	tableList= File.readlines()
	while tableList[-1]=='\n':					# handling empty lines at the end
		tableList.pop()
	for i, item in enumerate(tableList):
		item=item.replace("\n","")
		tableList[i]=item
	i=0
	tables={}								# dict of lists for storing table headers
	for j in range(len(tableList)):
	    if tableList[j]=="<begin_table>":
	        i=j
	    if tableList[j]=="<end_table>":    
	        tables[tableList[i+1]]=tableList[i+2:j]	
	File.close()
print tables       

##### Reading data from all csv files #####
tableDataC={}							# dict of tableName:Data in column order
tableDataR={}							# dict of tableName:Data in row order
tableTemp=[] 
for i in tables.keys():
	try:
		File = open(i+'.csv')
	except IOError:
		print i+'.csv' + ' does not exist!!'
		sys.exit(0)
	else:	
		reader = csv.reader(File)
		tableTemp = list(reader)
		tableDataR[i] = tableTemp
		tableTemp = convertRowsToCols(tableTemp)
		tableDataC[i]=tableTemp
		File.close()
print tableDataR

##### Parsing query #####
query = sys.argv[1]
parsed = sqlparse.parse(query)
tokens = parsed[0].tokens
cols=str(tokens[2])						# all columns requested
tabs=str(tokens[6])						# tables requested

# check if cols and tabs are actually present
# to-do

if isinstance(tokens[2],sqlparse.sql.Function):			# aggregate functions
	funcs=['distinct','max','min','avg','sum']	
	for f in funcs:
		if f in cols:
			print '%'
elif '*' in cols:										# select *
	printAllCols(tabs,tables,tableDataR)
elif isinstance(tokens[2],sqlparse.sql.Identifier):		
	printCols(cols,tabs,tables,tableDataR)
elif isinstance(tokens[2],sqlparse.sql.IdentifierList):
	printCols(cols,tabs,tables,tableDataR)		
