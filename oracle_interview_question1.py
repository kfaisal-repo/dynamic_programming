string="a string can have Many repeated words words we are not Looking at at amaan armaan armaan ajax abbu abbu abbu special charracter. but are looking at uniquely identifiable"

dictionary={}
for i in string.split(" "):
    i=i.lower()
    if i not in dictionary.keys():
        dictionary[i]=1
    else:
        dictionary[i] +=1
desc_list_values=sorted(dictionary.values(),reverse=True)

desc_list_values=desc_list_values[:5]

final_sort=[]

for i in sorted(set(desc_list_values),reverse=True):
    t= [k for k,v in dictionary.items() if v == i]
    final_sort += sorted(t)


print(final_sort[:5])
