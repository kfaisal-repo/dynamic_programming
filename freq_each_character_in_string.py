s="agrtydlkjglsdkjslknvlsknfs"

dictionary={}

for i in list(s):
    if i not in dictionary.keys():
        dictionary[i]=1

    else:
        dictionary[i] +=1
concatenated_string=""
for k,v in dictionary.items():
    concatenated_string =concatenated_string+k+str(v)

print(concatenated_string)



#print frequency of each character in a string - example- a1g2r1t1y1d2l4k4j2s4n2v1f1
