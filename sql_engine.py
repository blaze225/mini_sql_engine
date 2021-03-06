import sys
from sys import stdout
import csv
import sqlparse
from itertools import chain

def printAllCols(tabs,tables,tableDataR):	
	""" Printing all columns for a single table """
	tabs=tabs.replace(' ','')
	tabsList=tabs.split(',')
	for tab in tabsList:
		print ' '.join(tables[tab]),
	stdout.write("\n")	 
	for tab in tabsList:
		for i in tableDataR[tab]:
			print ' '.join(i)

def printAllColsWithJoinCommon(tabs,tables,tableDataR,col):
	""" tabs- list of tables, col- common joining column """
	data=[]
	headerList=[]
	pos1 = tables[tabs[0]].index(col)	# positions of col in both tables
	pos2 = tables[tabs[1]].index(col)
	for t in tabs:						# print headers with  col printed only once
		for c in tables[t]:
			headerList.append(c)
	headerList.reverse()
	headerList.remove(col)
	headerList.reverse()		
	print ' '.join(headerList)

	for r1 in tableDataR[tabs[0]]:
		for r2 in tableDataR[tabs[1]]:
			if r1[pos1]==r2[pos2]:
				del r2[pos2]
				data.append(list(chain(r1,r2)))
				break
	for i in data:
		print ' '.join(i)			

def printAllColsWithJoin(tabs,colsJoin,tables,tableDataR):
	""" tabs- list of tables, colsJoin- list of joining columns"""
	data=[]
	headerList=[]
	pos1 = tables[tabs[0]].index(colsJoin[0])	# positions of cols in both tables
	pos2 = tables[tabs[1]].index(colsJoin[1])
	for t in tabs:						# print headers 
		for c in tables[t]:
			headerList.append(c)
	headerList.remove(colsJoin[1])			# print headers with joining col printed only once	
	print ' '.join(headerList)

	for r1 in tableDataR[tabs[0]]:
		for r2 in tableDataR[tabs[1]]:
			if r1[pos1]==r2[pos2]:
				del r2[pos2]
				data.append(list(chain(r1,r2)))
				break
	for i in data:
		print ' '.join(i)

def printCrossProduct(tabs,tableDataR):
	""" cross product of two tables in tabs"""
	tabsList=tabs.split(',')
	data=[]
	for r1 in tableDataR[tabsList[0]]:
		for r2 in tableDataR[tabsList[1]]:
			data.append(list(chain(r1,r2)))
	for i in data:
		print ' '.join(i)

def getColIndices(cols,tables,tabName):
	""" Get indices of columns in cols in a list"""
	colList=cols.split(',')
	colIndices=[]
	for i in colList:
		colIndices.append(tables[tabName].index(i))
	return colIndices		

def printCols(cols,tabs,tables,tableDataR):
	""" Print multiple columns from a table """
	tabs=tabs.replace(' ','')			# 1 table
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

def applyAggregateFunc(cols,tables,tableDataC, aggr):
	""" apply aggregate function-aggr on cols """
	colList=cols.split(',')
	colNums=getColIndices(cols,tables,tabs)
	for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				print tables[tabs][i],
	stdout.write("\n")
	if aggr=='distinct':
		for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				result=[]
				for j in tableDataC[tabs][i]:
					if j not in result:
						result.append(j)
				print '\n'.join(result)		
	elif aggr=='max':
		for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				print max(map(int,tableDataC[tabs][i]))	
	elif aggr=='min':
		for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				print min(map(int,tableDataC[tabs][i]))
	elif aggr=='avg':
		for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				print sum(map(float,tableDataC[tabs][i]))/len(tableDataC[tabs][i])
	elif aggr=='sum':
		for i in range(len(tables[tabs])):			# table attribute names 
			if i in colNums:
				print sum(map(float,tableDataC[tabs][i]))	

def checkErrors(cols,tabs,tables):
	colList=cols.split(',')
	tabList=tabs.split(',')
	check=True
	colCheck=0
	for t in tabList:
		try:
			val = tables[t]
		except KeyError:
			print "Table "+ t + " not Found!!"
			sys.exit(0)
		if cols=='*':
			check=False
		for f in ['distinct','max','min','avg','sum']:
			if f in cols:
				check=False
		if check:		
			for c in colList:
				if c not in tables[t]:
					colCheck+=1				
	if colCheck ==len(tabList)*len(colList):
		print "Column "+c+" not Found!!"
		sys.exit(0)

def convertRowsToCols(tableTemp):
	lst = []
	for i in tableTemp[0]:
		lst.append([])
	for row in tableTemp:
		for i in range(len(row)):
			lst[i].append(row[i])
	return lst		

#################### Command line Agruments check #######################
if len(sys.argv) !=2:
	print 'Incorrect arguments given!'
	print 'usage: python sql_engine.py <sql_query>'
	sys.exit(0)

##################### Reading table headers from metadata.txt ##################
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
#print tables       

############################ Reading data from all csv files #########################
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
#print tableDataR

#################################### Parsing query #####################################
query = sys.argv[1]
parsed = sqlparse.parse(query)
tokens = parsed[0].tokens
where=False
for i in tokens:
	if isinstance(i,sqlparse.sql.Where):			# Check for WHERE clause
		where=True

cols=str(tokens[2])						# all columns requested
cols=cols.replace(' ','')
tabs=str(tokens[6])						# tables requested

if where:
	whereList=str(tokens[8]).replace(' ','').replace('where','').replace(';','').split('=')
	for i,item in enumerate(whereList):
		item=item.split('.')
		whereList[i]=item

checkErrors(cols,tabs,tables)			# check for errors

if isinstance(tokens[2],sqlparse.sql.Function):			# aggregate functions
	funcs=['distinct','max','min','avg','sum']	
	for f in funcs:
		if f in cols:
			if '(' not in str(tokens[2]) or ')' not in str(tokens[2]):
				print "Error:No braces with aggregate function!"
				sys.exit(0)
			elif ',' in cols[cols.find('(')+1:cols.find(')')]:
				print "Error:Too many columns given in aggregate function!"
				sys.exit(0)
			else:
				cols=cols[cols.find('(')+1:cols.find(')')]
				checkErrors(cols,tabs,tables)
				applyAggregateFunc(cols,tables,tableDataC, f)
elif '*' in cols:										# select *
	if where:											# JOIN condition present
		tabs=[]
		colsJoin=[]
		for i in whereList:
			tabs.append(i[0].replace(' ',''))
			colsJoin.append(i[1].replace(' ',''))
		if whereList[0][1]==whereList[1][1]:			# JOIN with common column
			printAllColsWithJoinCommon(tabs,tables,tableDataR,whereList[0][1])
		else:
			printAllColsWithJoin(tabs,colsJoin,tables,tableDataR)

	else:
		if len(tabs.split(','))>1:
			printCrossProduct(tabs,tableDataR)
		else:	
			printAllCols(tabs,tables,tableDataR)
elif isinstance(tokens[2],sqlparse.sql.Identifier):		# one column
	printCols(cols,tabs,tables,tableDataR)
elif isinstance(tokens[2],sqlparse.sql.IdentifierList):	# multiple columns
	printCols(cols,tabs,tables,tableDataR)		
