import math
'''class euler:
    def __init__(self):
        pass'''

def lcm(x,y):
    if y>x:
        a=x
        x=y
        y=a
    else:
        a=x
    while True:
        if a%y==0 and a%x==0:
            return a
        else:
            a+=1

def gcf(x,y):
    if x>y:
        a=y
        y=x
        x=a
        a=x
    else:
        a=x
    for i in range(x,0,-1):
        if x%i==0 and y%i==0:
            return i
        else:
            pass

def divisors(x):
    array=[]
    for i in range(1,x+1):
        if x%i==0:
            array.append(i)
    return array

def prime(x):
    if x==1:
        return False
    if x==0:
        return False
    for i in range(2,x):
        if x%i==0:
            return False
    return True

def prime_divisors(x):
    array=[]
    for i in range(2,x):
        if x%i==0 and prime(i):
            array.append(i)
    return array

def prime_factors(x):
    array=[]
    o=x
    i=2
    while i<=x:
        if x%i==0:
            array.append(i)
            x/=i
            i=2
        else:
            i+=1
    if len(array)==0:
        array.append(o)
    return array

def sieve(x):
    array=[]
    for i in range(2,x):
        if prime(i):
            array.append(i)
    return array

def sub_sets(array):
    try:
        if array==int(array) or array==str(array):
            array=list(str(array))    
    except:
        pass
    ans=[]
    for i in range(len(array)):
        for j in range(len(array)-i):
            ans.append(array[i:len(array)-j])
    return(ans)
    
def proper_divisors(x):
    return divisors(x)[:-1]

def amicable(x,y):
    if x==sum(proper_divisors(y)) and y==sum(proper_divisors(x)):
        return True
    return False

def perfect(x):
    if x==sum(proper_divisors(x)):
        return True
    return False

def index_prime(x):
    a=2
    count=0
    y=0
    while y<x:
        if prime(a):
            count=a
            y+=1
        a+=1
    return count

def sqrt(x):
    return math.sqrt(x)

def totient(x):
    count=1
    for i in range(2,x):
        bug=0
        for j in range(2,i+1):
            if i%j==0 and x%j==0:
                break
            else:
                bug+=1
                if bug==i-1:
                    count+=1
    return count


def perfect_power(n):
    base=2
    power=0
    while True:
        if base**power==n:
            return True
        elif base**power>n:
            base+=1
            power=0
            if base**(power+1)>n or base==n:
                return False
        power+=1

def nth_prime(x):
    for i in range(1,x):
        if index_prime(i)==x:
            return i

def consecutive_primes(x):
    if len(x)==1:
        return False
    for i in range(1,len(x)):
        if nth_prime(x[i])!=(nth_prime(x[i-1])+1):
            return False
    return True

def powerful(n):
    if n==1:
        return True
    array=prime_factors(n)
    count=0
    for i in range(len(array)):
        if n%(array[i]**2)==0:
            count+=1
            if count==len(array):
                return True
        else:
            return False

def achilles(x):
    if powerful(x)==True and perfect_power(x)==False:
        return True
    return False

def fibonacci(start,length):
    if start==0:
        array=[start,1]
        length-=2
    elif start==1:
        array=[start,start]
        length-=1
    for i in range(start,length):
        array.append(array[-1]+array[-2])
    return array

def palindrome(x):
    if int(str(x)[::-1])==x:
        return True
    return False

def pentagonal_index(x):
    return int(x*(3*x-1)/2)

def is_pentagonal(x):
    for i in range(1,x+1):
        if pentagonal_index(i)==x:
            return True
        elif pentagonal_index(i)>x:
            return False

'''
def bell_index(x):
    x-=1
    if x==0 or x==1:
        return 1
    ans=1
    for i in range(1,x):
        ans+=((x-1)/i)*bell_index(i+1)
    return ans
'''

def bell_index(x):
    array=[1]
    #print(array[0:]) #Uncomment this line and the other commented line 6 lines below this one to show Bell Triangle
    for i in range(x):
        if i!=0:
            array.append(array[-1])
            for k in range(i):
                array.append(array[-1]+array[-1-i])
            #print(array[len(array)-1-i:])
    return array[len(array)-1-i]

def is_bell(x):
    for i in range(1,x+1):
        if bell_index(i)==x:
            return True
        elif bell_index(i)>x:
            return False

#print(lcm(326,411))
#print(gcf(24,16))
#print(divisors(0))
#print(prime(2))
#print(prime_divisors(132))
#print(prime_factors(132))
#print(sieve(132))
#print(sub_sets([1,2,3]))
#print(proper_divisors(60))
#print(amicable(2620,2924))
#print(perfect(8128))
#print(index_prime(129))
#print(sqrt(6))
#print(totient(10))
#print(perfect_power(4096))
#print(nth_prime(17))
#print(consecutive_primes([2,3,5,7,11,13]))
#print(powerful(25))
#print(achilles(432))
#print(fibonacci(1,9))
#print(palindrome(1234321))
#print(pentagonal_index(8))
#print(is_pentagonal(15))
#print(bell_index(6))
#print(is_bell(203))

'''
Friedman number
'''