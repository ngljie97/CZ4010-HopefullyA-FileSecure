import random
from math import gcd

def generateRandomPrime(): # P
    prime_list = listOfPrimes(100,250)
    randomPrime = random.choice(prime_list)
    return randomPrime

def listOfPrimes(x,y): 
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    return prime_list

def generateRandomPrimitive(): # G
    primitive_list = listOfPrimitives(P)
    randomPrimitive = random.choice(primitive_list)
    return randomPrimitive

def listOfPrimitives(n):
    primitive_list = []
    for i in range(2, n, 1):
        if (gcd(i, n) == 1):
            primitive_list.append(i)
    
    return primitive_list

def publicKey(n): # User's public key, n is user secret key
    key = int(pow(G,n,P))
    return key

def secretKey(pk, n): # pk is the other party public key, n is user secret key
    skey = int(pow(pk,n,P))
    return skey

P = generateRandomPrime() # mod n / large generated prime number (known)
G = generateRandomPrimitive() # known number


        