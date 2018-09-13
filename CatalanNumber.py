C=[]

def returnCatalanNumber(number):

    sum=0
    for i in range(0,number):
        sum = sum + (C[i] * C[number-1-i])
    return sum

C.insert(0,1)
C.insert(1,1)
N=int(input())

for i in range(2,N):
    C.insert(i,returnCatalanNumber(i))

print(*C)

