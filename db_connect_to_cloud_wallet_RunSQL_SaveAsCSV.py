import os

import cx_Oracle
import csv,re,pprint

warehouse_sql_list = [f for f in os.listdir('warehouse_queries') if re.match(r'.*.sql', f)]
source_sql_list = [f for f in os.listdir('source_queries') if re.match(r'.*.sql', f)]


# setting environment variable for the wallet location
os.environ["TNS_ADMIN"] = "/Users/fafakhan/Downloads/Wallet_DBPIPELINE"
dsnStr = "dbpipeline_low"
conction = cx_Oracle.connect(user="CUST3_IADW", password="Cust2Fusion5#5", dsn=dsnStr)

csr = conction.cursor()

for wsl in warehouse_sql_list:
    sql_content=open("warehouse_queries/"+wsl,"r").readlines()
    sql_content=" ".join(map(str, sql_content))
    print("BEFORE REPLACE")
    print(sql_content)
    print("AFTER REPLACE")

    sql_content= " ".join(sql_content.splitlines())
    print(sql_content.strip())
    faisal=csr.execute(sql_content)
    csv_headers=csr.description
    a1=[i[0] for i in csv_headers]

    print(a1)
    data=csr.fetchall()

    fileNameOnly = wsl[:wsl.find(".sql") + len(".sql")]
    fileNameOnly=fileNameOnly.replace(".sql","")
    fileNameOnly=fileNameOnly+"_mod.csv"

    with open(fileNameOnly,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(a1)
        csv_out.writerows(data)

conction.close()

################


conction_source =cx_Oracle.connect('fusion', 'welcome1', 'slc12uxz.us.oracle.com:1521/r13csmcf_b')

csr = conction_source.cursor()

for ssl in source_sql_list:
    sql_content=open("source_queries/"+ssl,"r").readlines()
    sql_content=" ".join(map(str, sql_content))
    print("BEFORE REPLACE")
    print(sql_content)
    print("AFTER REPLACE")



    sql_content= " ".join(sql_content.splitlines())
    print(sql_content.strip())
    csr.execute(sql_content)
    csv_headers=csr.description
    a1=[i[0] for i in csv_headers]

    print(a1)
    data=csr.fetchall()

    fileNameOnly = ssl[:ssl.find(".sql") + len(".sql")]
    fileNameOnly=fileNameOnly.replace(".sql","")
    fileNameOnly=fileNameOnly+"_bench.csv"

    with open(fileNameOnly,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(a1)
        csv_out.writerows(data)

conction_source.close()

################

