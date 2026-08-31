# Basic Level Questions
'''
a = int(input())

if a >= 0:
    print("Positive")
else:
    print("Negative")'''

'''
age=int(input())

if age>=18:
    print("You are eligible to Vote")
else:
    print("Not eligible")'''

'''a=int(input())
b=int(input())

if a>b:
    print(f"{a}")
else:
    print()'''
'''
a=input()

if a.isalpha():
    print("Letter")
else:
    print("Not Letter")'''

#conditional statements
'''
n=int(input())
if n>=0:
    print("postive number")
else:
    print("negative number")'''

# greatest number

'''n=int(input())
s=int(input())
d=int(input())
if n>s and n>d:
    print(f"greatest number {n}")
elif s>n and s>d:
    print(f"greatest number{s}")
elif d>n and d>s:
    print(f"greatest number9{d}")
else:
    print()'''

#check wheather three digit number or not

'''a=int(input())

if  100 <=abs(a) <=999:
    print(f"its a three digit number")

else:
    print(f"Its not a three digit number")'''

#if elif else for tempreature
'''
a=int(input())
if a>30:
    print("Its hot")
elif a>15 and a<30:
    print("pleasent")
else:
    print("cold")'''

#shapes
'''n=int(input())
if n==3:
    print("Its a triangle")
elif n==4:
    print("Its a Quadraliteral")
elif n==5:
    print("Its a Pentagon")
else:
    print("Its Unknown shape")'''

# nested conditional statements
'''char=input();
if char.isalpha():
    if char.isupper():
        print("Its a upper letter")
    else:
        print("Its a lower letter")
else:
    print("its not a letter")
'''

#prime number

'''n=int(input())

if n>1:
    if n%2!=0:
        print("its a prime number")
    else:
        print("Its not a prime number")
else:
    print("its not a number")'''


#multiple of number

'''n=int(input())
if n%5==0:
    if n%2==0:
        print("its is even number")
    else:
        print("its is odd number")
else:
    print("its not multiple of 5")
    '''

#multiple of a number postive or negative
'''
n=int(input())
if n%5==0:
    if n>0:
        print("Its is a multiple of 5 and postive number")
    elif n<0:
        print("Its is a multiple of 5negative number")
    else:
        print("Its zero")
else:
    print("Its not multiple of 5")
'''
#palindrome string with slicing
'''
n=input()

if n==n[::-1] :
    print("Palindrome")
else:
    print("Not Palindrome")

'''
# without using slicing
'''
n=input()
res=""
for i in range(len(n)-1,-1,-1):
    res=res+n[i]
if n==res:
    print("Palindrome")
        
else:
    print("Not Palindrome")
        '''
#palindrome using number
'''
n=int(input())
temp=0

if n%10:
    temp=temp*10+1

    print("Palindrome")
else:
    print("Not Palindrome")'''

#creating class and constructor , instance variables
'''
class car:
    def __init__(self,name,color,price):
        self.carname=name
        self.carcolor=color
        self.carprice=price

s1=car("Bugati","Red","2,00,000,0000")
print("Car name is:", s1.carname)
print("car color is:", s1.carcolor)
print("car price is:", s1.carprice)'''

#patterns
'''n=int(input())
for i in range(n-1,1):
    for j in range(n-i,1):
        print("*",end="")
    print()
'''
'''
n=int(input())
for i in range(n,0,-1):

    for j in range(n-i):
        print(" ",end=" ")
    for j in range(2*i-1):
        print("*",end=" ")
    print()
for i in range(1,n+1):

    for j in range(n-i):
        print(" ",end=" ")
    for j in range(2*i-1):
        print("*",end=" ")
    print()'''
#Hallow method
''''n = int(input())
for i in range(n):

    for j in range(n):

        if i==0 or i==n-1 or j==0 or j==n-1:


            print("*",end=" ")
        else:
            print(" ",end=" ")
    print()''''



