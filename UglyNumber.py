def gcd_divide_throw_out_divisor(n,i):

    while n % i ==0:
        n /=i
    return n


def IsAnUglyNumber(num):
    num=gcd_divide_throw_out_divisor(num,2)
    num = gcd_divide_throw_out_divisor(num, 3)
    num = gcd_divide_throw_out_divisor(num, 5)
    if num ==1:
        return 1
    else:
        return 0


def getMeNthUglyNumber(N):
    count=0
    i=1
    while count < N:
        if IsAnUglyNumber(i):
            count +=1
        i+=1
    return i-1

print(getMeNthUglyNumber(150))











