T=int(input())
input_list=[]
def getMinimum(n):
    if int(n) >= 10:
        lst=list(n)
        lst_final=[]
        for x in range(len(lst)):
            lst_final.append(int("".join(lst[:x]+lst[x+1:])))
        return min(lst_final)
    else:
        return n

for i in range(T):
    input_list.append(input())

for i in input_list:
    print(getMinimum(i))
