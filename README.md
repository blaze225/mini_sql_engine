# mini_sql_engine
## Dataset:
1. csv files for tables.

   i. If a file is named File1.csv, the table name would be File1 .
   
  ii. There will be no tab​ -separation or space-​ separation,so you are not required to handle it but you have to make sure to take care of both csv file type cases: the one where values are in double quotes, and the one where values are without quotes.
  
2. All the elements in files would be integers only.
3. A file namedmetadata.txt (note the extension) will be given to you, which will have the following structure for each table:
<begin_table>
<table_name>
<attribute1>
....
<attributeN>
<end_table>

## Type of Queries:
Your code will be expected to run the following set of queries.

1. Select all records: Select * from table_name;

2. Aggregate functions: Simple aggregate functions on a single
column. Sum, average, max and min. They will be very trivial
given that the data is only numbers: select max(col1) from
table1;

3. Project Columns​ (could be any number of columns) from one or
more tables : Select col1, col2 from table_name;

4. Select/project with distinct from one table​ : select distinct
col1, col2 from table_name;

5. Select with where from one or more tables​ : select col1,col2
from table1,table2 where col1 = 10 AND col2 = 20;
  a. In the where queries, there would be a maximum of one
AND/OR operator with no NOT operators. (Bonus marks
will be awarded if you handle cases with multiple AND/OR
operators)

6. Projection of one or more(including all the columns) from
two tables with one join condition​ :

  a. select * from table1, table2 where table1.col1=table2.col2;
  
  b. select col1,col2 from table1,table2 where table1.col1 =
table2.col2;

  c. The joining column should be printed only once​ . No
repetitions.( Bonus marks will be awarded if you handle
cases with multiple tables join)
