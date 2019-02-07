import csv
import collections
import webbrowser
from pprint import pprint

#convert output to csv


column_names1=[]
column_names2=[]
flag_column_names_matched=False
column_names_html=""
primary_key_column='SOURCE_RECORD_ID'
mydict1={}
mydict2={}
missing_records_html_outer=""
extra_recs_html_outer=""
diff_recs_html_outer=""

files=['export_bench.csv','export_mod.csv']

with open(files[0]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if not row:
            continue
        if line_count == 0:
            s=", ".join(row)
            column_names1=s.strip().split(',')
            column_names1 = [x.strip(' ') for x in column_names1]
            line_count += 1
        else:
            line_count += 1
            index_of_primary_key_column = column_names1.index(primary_key_column)
            mydict1[row[index_of_primary_key_column]] = row

no_of_lines1 = line_count - 1
#pprint(mydict1)

with open(files[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if not row:
            continue
        if line_count == 0:
            s=", ".join(row)
            column_names2 = s.strip().split(',')
            column_names2 = [x.strip(' ') for x in column_names2]
            line_count += 1
        else:
            line_count += 1
            index_of_primary_key_column = column_names2.index(primary_key_column)
            mydict2[row[index_of_primary_key_column]] = row

no_of_lines2=line_count - 1

def checkAlienRecordsInDestination(source_dict,destination_dict):
    alien_records = {k: destination_dict[k] for k in destination_dict if k not in source_dict}
    if alien_records:
        print("\nNumber of alien records (New records found in warehouse table): ",len(alien_records))

        print("\nAlien record list:")
        for key in alien_records:
            print(alien_records[key],"\n")
    return (len(alien_records),alien_records)

def checkMissingRecords(source_dict,destination_dict):
    missing_records = {k: source_dict[k] for k in source_dict if k not in destination_dict}
    if missing_records:
        print("\nNumber of missing records: ",len(missing_records))
        print("\nMissing records List:")
        for key in missing_records:
            print(missing_records[key],"\n")
    return missing_records

def compareDataInDictionaries(source_dict,destination_dict):
    shared_items = {k: source_dict[k] for k in source_dict if k in destination_dict and source_dict[k] == destination_dict[k]}
    print("\nOnly ",len(shared_items)," records match")

    not_same_items = {k: [source_dict[k],destination_dict[k]] for k in source_dict if k in destination_dict and source_dict[k] != destination_dict[k]}
    if not_same_items:
        print("\nSee Differences below ...\n")


    return (shared_items,not_same_items)
print("\n======================Basic Schema Validation Report=====================\n")


if len(column_names1) == len(column_names2):
    print("\nNumber of column are same","\tSOURCE TABLE -",len(column_names1),"columns","WAREHOUSE TABLE -",len(column_names2),"columns")
else:
    print("\nNumber of column are NOT same","\tSOURCE TABLE -",len(column_names1),"columns","WAREHOUSE TABLE -",len(column_names2),"columns")


compare = lambda x, y: \
    collections.Counter(x) == collections.Counter(y)
if compare(column_names1,column_names2):
    print("\nAll column names match")
    flag_column_names_matched=True
else:
    diff=list(set(column_names1)-set(column_names2))
    print("\nAll column names DO NOT match",diff,"-- these columns are not present in the warehouse schema")


if no_of_lines1==no_of_lines2:

    print("\nNumber of records are same","\tSOURCE TABLE -",no_of_lines1,"lines","WAREHOUSE TABLE -",no_of_lines2,"lines")
else:

    print("\nNumber of records are NOT same","\tSOURCE TABLE -",no_of_lines1,"lines","WAREHOUSE TABLE -",no_of_lines2,"lines")


missing_records=checkMissingRecords(mydict1,mydict2)
(same_recs,diff_recs)=compareDataInDictionaries(mydict1,mydict2)
(alien_records_number,extra_recs)=checkAlienRecordsInDestination(mydict1,mydict2)
print("\n\n======================Basic Schema Validation Report Ends=====================\n")

# print(column_names1)
#
# for k in output:
#
#     diff=mydict1[k] - mydict2[k]
#     if not diff:
#         print("faisal inside")
#         diff=mydict2[k] - mydict1[k]
#
#     print(diff)


f = open('helloworld.html','w')
titles='''
<title>Page Title</title>
'''
styles='''
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
'''
heading1="<h1>Schema Difference Evaluator</h1>"
table_name="<p>Table Name - "+((files[0]).split('_bench'))[0]+"</p>"
table_heading="<h3>Basic properties (Schema level)</h3>"

full_table_header1='''
    <tr>
    <th>Attributes</th>
    <th>Source Table</th>
    <th>Warehouse Table</th>
  </tr>
'''
no_of_cols="<tr><td>Total number of columns</td><td>"+str(len(column_names1))+"</td><td>"+str(len(column_names1))+"</td></tr>"
no_of_recs="<tr><td>Total number of records</td><td>"+str(no_of_lines1)+"</td><td>"+str(no_of_lines2)+"</td></tr>"
names_match="<tr><td>Do column names match ? </td><td>"+str(flag_column_names_matched)+"</td><td>"+str(flag_column_names_matched)+"</td></tr>"
no_of_extra_records="<tr><td>Number of extra records from warehouse table:</td><td>"+str(alien_records_number)+"</td></tr>"
no_of_missing_records="<tr><td>Number of missing records from warehouse table:</td><td>"+str(len(missing_records))+"</td></tr>"
exactly_matching_records="<tr><td>Number of exactly matching records in source and warehouse tables:</td><td>"+str(len(same_recs))+"</td></tr>"

full_table1="<table>"+full_table_header1+no_of_cols+no_of_recs+names_match+no_of_extra_records+no_of_missing_records+exactly_matching_records+"</table>"




full_table2='''
<h3>Advance properties (Data level)</h3>
<p><h3>Missing Records in warehouse tables</h3></p>
'''

for i in column_names1:
    column_names_html=column_names_html+"<th>"+i+"</th>"
column_names_html="<tr>"+column_names_html+"</tr>"

for i in missing_records:
    missing_records_html_inner=""
    for j in missing_records[i]:

        missing_records_html_inner=missing_records_html_inner+"<td>"+j+"</td>"

    missing_records_html_outer=missing_records_html_outer+"<tr>"+missing_records_html_inner+"</tr>"

full_table3='''
<p><h3>Extra Records in warehouse tables</h3></p>
'''

for i in extra_recs:
    extra_recs_html_inner=""
    for j in extra_recs[i]:
        extra_recs_html_inner=extra_recs_html_inner+"<td>"+j+"</td>"
    extra_recs_html_outer=extra_recs_html_outer+"<tr>"+extra_recs_html_inner+"</tr>"

full_table4='''
<p><h3>Different Records in warehouse tables</h3></p>
'''
print("DIFFERNT RECORDS FAILLLLLL",len(diff_recs))
pprint(diff_recs)

for i in diff_recs:
    source_list=diff_recs[i][0]
    warehouse_list=diff_recs[i][1]
    diff_recs_html_inner_source=""
    diff_recs_html_inner_warehouse = ""

    for j in source_list:
        k=warehouse_list[source_list.index(j)]
        print(source_list,warehouse_list)
        if j == k:
            diff_recs_html_inner_source = diff_recs_html_inner_source + "<td>" + j + "</td>"
            diff_recs_html_inner_warehouse = diff_recs_html_inner_warehouse + "<td>" + k + "</td>"
        else:
            diff_recs_html_inner_source = diff_recs_html_inner_source + "<td bgcolor=\"#FF0000\">" + j + "</td>"
            diff_recs_html_inner_warehouse = diff_recs_html_inner_warehouse + "<td bgcolor=\"#FF0000\">" + k + "</td>"
    diff_recs_html_outer=diff_recs_html_outer+"<tr>"+diff_recs_html_inner_source+"</tr>"+"<tr>"+diff_recs_html_inner_warehouse+"</tr>"

advanced_table=full_table2+"<table>"+column_names_html+missing_records_html_outer+"</table>"+full_table3+"<table>"+column_names_html+extra_recs_html_outer+\
               "</table>"+full_table4+"<table>"+column_names_html+diff_recs_html_outer+"</table>"

base_table="<html><head>"+titles+styles+"</head><body>"+heading1+table_name+table_heading+full_table1+advanced_table+"</body></html>"


f.write(base_table)

f.close()

#Change path to reflect file location
filename = 'file:///Users/fafakhan/PycharmProjects/DW_Validation/' + 'helloworld.html'
webbrowser.open_new_tab(filename)
