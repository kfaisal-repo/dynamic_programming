def getBinomialCoffecientInLinearComplexity(n,r):
    res=1
    if r > n-r:
        r = n-r

    for i in range(r):
        res = res *(n-i)
        res = res/(i+1)
    return res
# print(getBinomialCoffecientInLinearComplexity(5,3))
# print(getBinomialCoffecientInLinearComplexity(15,2))
# print(getBinomialCoffecientInLinearComplexity(6,4))
