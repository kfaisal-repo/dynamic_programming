num_testcases=int(input())
data_diction={}
dd={}
for i in range(0,num_testcases):
    num_lines = int(input())
    for j in range(0,num_lines):
        dd[j]=input().split(" ")
    data_diction[i]=dd
    dd={}
for i in data_diction.values():
    kl=i.values()
    shtlst={}
    counter=0
    for j in kl:
        if (j[0] in shtlst.keys() and shtlst[j[0]] == j[1]) or (j[0] not in shtlst.keys()):
            shtlst[j[0]]=j[1]
            counter+=1
        else:
            continue
    print(counter)
