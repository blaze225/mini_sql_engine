import csv

### Reading table headers from metadata.txt ###
File = open("metadata.txt")
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
	File = open(i[0]+'.csv')
	reader = csv.reader(File)
	tableTemp = list(reader)
	tableData[i[0]]=tableTemp

print tableData	

