from sympy.solvers import solve
from sympy import Poly, Eq, Function, exp
from sympy import Symbol
from sympy.abc import x, y, z, a, b
import tkinter
from tkinter import *
from tabulate import tabulate
import string
from fractions import Fraction
from mpmath import *
import numpy as np
from scipy import *
import math
import cmath
import time
import sys
import keyboard
import matplotlib.pyplot as plt

val = ""
def ShowCalculator():
    global bt
    global do_it
    global tk
    global clear
    tk = Tk()
    global data
    data= StringVar()
    lbl=Label(
        tk,
        text="Label",
        anchor=SE,
        font=("Verdana",20),
        textvariable=data,
        background="#ffffff",
        fg="#000000",
    )
    lbl.grid(row = 0, column = 0)
    btn1 = Button(tk, text="1", command= lambda: bt("1"))
    btn1.grid(row = 1, column = 0, sticky = W)
    btn2 = Button(tk, text="2", command= lambda: bt("2"))
    btn2.grid(row = 1, column = 1, sticky = W)
    btn3 = Button(tk, text="3", command= lambda: bt("3"))
    btn3.grid(row = 1, column = 2, sticky = W)
    plus = Button(tk, text="+", command= lambda: bt("+"))
    plus.grid(row = 1, column = 3, sticky = W)
    btn4 = Button(tk, text="4", command= lambda: bt("4"))
    btn4.grid(row = 2, column = 0, sticky = W)
    btn5 = Button(tk, text="5", command= lambda: bt("5"))
    btn5.grid(row = 2, column = 1, sticky = W)
    btn6 = Button(tk, text="6", command= lambda: bt("6"))
    btn6.grid(row = 2, column = 2, sticky = W)
    minus = Button(tk, text="-", command= lambda: bt("-"))
    minus.grid(row = 2, column = 3, sticky = W)
    btn7 = Button(tk, text="7", command= lambda: bt("7"))
    btn7.grid(row = 3, column = 0, sticky = W)
    btn8 = Button(tk, text="8", command= lambda: bt("8"))
    btn8.grid(row = 3, column = 1, sticky = W)
    btn9 = Button(tk, text="9", command= lambda: bt("9"))
    btn9.grid(row = 3, column = 2, sticky = W)
    times = Button(tk, text="*", command= lambda: bt("*"))
    times.grid(row = 3, column = 3, sticky = W)
    btn0 = Button(tk, text="0", command= lambda: bt("0"))
    btn0.grid(row = 4, column = 0, sticky = W)
    dot = Button(tk, text=".", command= lambda: bt("."))
    dot.grid(row = 4, column = 1, sticky = W)
    divide = Button(tk, text="/", command= lambda: bt("/"))
    divide.grid(row = 4, column = 2, sticky = W)
    clr = Button(tk, text="C", command= lambda: clear())
    clr.grid(row = 4, column = 3, sticky = W)
    eq = Button(tk, text="=", command= lambda: do_it())
    eq.grid(row = 5, column = 0, sticky = W)
def HideCalculator():
    tk.destroy()
def bt(x):
    global val
    val = val + x
    data.set(val)
def do_it():
    global val
    y = eval(val)
    data.set(y)
    ans = val
    val=""
def clear():
    global val
    val =""
    data.set(val)
    


    
def add(a, b):
    return a+b
def subtract(a, b):
    return a-b
def multiply(a, b):
    return a*b
def divide(a, b):
    return a/b
def power(a, b):
    x=1
    while b > 0:
        x *=a
        b -=1
    return x
def recLimit(a):
    messagebox.askyesno("RECURSION SETTINGS", "Setting your recursion limit may slow your laptop or cause a crash. Proceed with caution. Do You wish to continue?")
def sqrt(a):
    return math.sqrt(a)

def addFraction(a, b):
    ans = Fraction(a) + Fraction(b)
    return str(ans)
def subtractFraction(a, b):
    ans = Fraction(a) - Fraction(b)
    return str(ans)
def multiplyFraction(a, b):
    ans = Fraction(a) * Fraction(b)
    return str(ans)
def divideFraction(a, b):
    ans = Fraction(a) / Fraction(b)
    return str(ans)
def simplifyFraction(a):
    return str(Fraction(a).limit_denominator())

def root(a, b):
    x = a**(1/b)
    y = round(x)
    if y-x <= 0.000000000000001:
        if x**(b) != a:
            return y
        else:
            return x
    elif y-x >= -0.000000000000001:
        if x**(b) != a and y-x<0:
            return y
        else:
            return x
    else:
        return x
    
def log(a, b):
    return math.log(a, b)
def sf(a, b):
    rounded = round(a, b - int(math.floor(math.log10(abs(a)))) - 1)
    return rounded
def absVal(a):
    return math.fabs(a)
def remainder(a, b):
    return math.remainder(a, b)
def toDegrees(a):
    return math.degrees(a)
def toRadians(a):
    return math.radians(a)

def HCF(a, b):
    a, b = max(a, b), min(a, b)
    while b!=0:
        a, b = b, a % b
    return a
def LCM(a, b):
    return (a*b)/HCF(a, b)
def primeFactors(n):
    while n % 2 == 0:
            print(2)
            n = n / 2  
    for i in range(3,int(math.sqrt(n))+1,2):
            while n % i== 0:
                    print(i)
                    n = n / i
    if n > 2:
            print(n)

def factorial(a):
    x = 1
    while a > 0:
        x *=a
        a -=1
    return x
def checkPrime(num):
    x = False
    for i in range(2, num):
        if num % i == 0:
            x = True
    if x == True:
        return False
    else:
        return True
def primeNumberPrinter(low, high):
    for num in range(low, high+1):
        if num > 1:
            for i in range(2, num):
                if num % i == 0:
                    break
            else:
                print(num)
def perfectSquare(num):
    root = math.sqrt(num)

    if math.trunc(root)-root==0:
        return True
    else:
        return False
def perfectSquarePrinter(low, high):
    for i in range(low, high):
        if perfectSquare(i	) == True:
            print(i)
def PerfectRootCheck(a, b):
    x = root(a, b)
    if x % 1 == 0:
        return True
    else:
        return False
def fibonacci(n):
    x = (((((1+math.sqrt(5))/2)**n)-((((1-math.sqrt(5))/2)**n))))/math.sqrt(5)
    return round(x)
def fibonacciCheck(n):
    return perfectSquareCheck(5*n*n + 4) or perfectSquareCheck(5*n*n - 4)
def fibonacciPrinter(low, high):
    for i in range(low, high+1):
        if fibonacciCheck(i) == True:
            print(i)
            
def divis2Check(num):
    if num % 2 == 0:
        return True
    else:
        return False
def divis3Check(num):
    if num % 3 == 0:
        return True
    else:
        return False
def divis4Check(num):
    if num % 4 == 0:
        return True
    else:
        return False
def divis5Check(num):
    if num % 5 == 0:
        return True
    else:
        return False
def divis6Check(num):
    if num % 6 == 0:
        return True
    else:
        return False
def divis7Check(num):
    if num % 7 == 0:
        return True
    else:
        return False
def divis8Check(num):
    if num % 8 == 0:
        return True
    else:
        return False
def divis9Check(num):
    if num % 9 == 0:
        return True
    else:
        return False
def divisCheck(num, num2):
    if num % num2 == 0:
        return True
    else:
        return False
    
def PercentagetoDecimal(percentage):
    return p / 100
def PerToFrac(p):
    dec = p / 100
    fraction = Fraction(dec)
    return str(fraction)
def PercentagetoFraction(percentage):
    fracOutput = PertoFrac(p)
    return "{0}".format(fracOutput)
def FractiontoDecimal(fraction):
    dec = f
    return str(round(dec, 5))
def FractiontoPercentage(fraction):
    return f * 100
def DecimaltoPercentage(decimal):
    percentage = "{:.0%}".format(d)
    return str(percentage)
def DecimaltoFraction(decimal):
    return str(Fraction(d).limit_denominator())

def triangleArea(l, w):
    return (l*w)/2
def trapeziumArea(a, b, h):
    return (a+b)/h
def paraArea(b, h):
    return b*h
def circleCircumference(r):
    return 2*math.pi*r
def circleArea(r):
    return math.pi*(r**2)
def sphereVolume(r):
    return 4/3*math.pi*(r**3)
def sphereArea(r):
    return 4*math.pi*(r**2)
def sphereDiametre(r):
    return 2*r
def surfaceArea(a, b, c):
    d = a*b
    e = a*c
    f = b*c
    return 2*(d+e+f)
def volume(a, b, c):
    return a*b*c
def cylinderVolume(r, h):
    return (math.pi*(r**2))*h
def cylinderArea(r, h):
    return (2*math.pi*r*h)+(2*math.pi*(r**2))
def cylinderDiametre(v, h):
    return 2*(math.sqrt(v/math.pi*h))
def cylinderHeight(v, r):
    return v/(math.pi*(r**2))
def cylindeRadius(h, A):
    return round(0.5*math.sqrt(h**2 + 2*(A/math.pi))-h/2, 5)
def coneArea(r, h):
    pi = math.pi
    area = pi*r*(r + math.sqrt(h**2 + r**2))
    return round(area, 5)
def coneVolume(r, h):
    pi = math.pi
    vol = pi*r**2*(h/3)
    return round(vol, 5)
def coneRadius(h, vol):
    pi = math.pi
    rad = math.sqrt(3*(vol/(pi*h)))
    return round(rad, 5)
def coneHeight(r, vol):
    pi = math.pi
    height = 3*(vol/(pi*r**2))
    return round(height, 5)

def sin(a):
    return math.sin(a)
def cos(a):
    return math.cos(a)
def tan(a):
    return math.tan(a)
def asin(a):
    return math.asin(a)
def acos(a):
    return math.acos(a)
def atan(a):
    return math.atan(a)
def sinh(a):
    return math.sinh(a)
def cosh(a):
    return math.cosh(a)
def tanh(a):
    return math.tanh(a)
def asinh(a):
    return math.asinh(a)
def acosh(a):
    return math.acosh(a)
def atanh(a):
    return math.atanh(a)
def sec(a):
    return round(1/cos(a), 5)
def csc(a):
    return round(1/sin(a), 5)
def cot(a):
    return round(1/tan(a), 5)
def gamma(a):
    return math.gamma(a)
def lgamma(a):
    return math.lgamma(a)

def pytheoromside(a, b):
    if a > c:
        a1 = a*ad
        b1 = b*b
        c1 = a1 - b1
        c = math.sqrt(c1)
    else:
        a1 = a*a
        b1 = b*b
        c1 = b1 - a1
        c = math.sqrt(c1)
    return c
def pytheorom(a, b):
    a1 = a*a
    b1 = b*b
    c1 = a1 + b1
    c = math.sqrt(c1)
    return c
def cos_rule(c, b, A):
    c1 *= c
    b1 *= b
    A1 = math.cos(A)
    thing = A1*c*b
    ans = b1 + a1 - thing
    answer = math.sqrt(answer)
    return answer
def areabytan(n, s):
    s1 = s*s
    up = n*s1
    intan = 180/n
    tanpart = math.tan(intan)
    down = 4*tanpart
    ans = up/down
    return ans
def pythagoreanTriplets(n):
  for b in range(n):
    for a in range(1, b):
        c = math.sqrt( a * a + b * b)
        if c % 1 == 0:
            print(a, b, int(c))
def pythagoreanTripletsCheck(a, b, c):
    if (a ** 2) + (b ** 2) == (c ** 2):
        return True
    else:
        return False
    
def speedCalc(d, t):
    return d/t
def distCalc(s, t):
    return s*t
def timeCalc(s, d):
    return s*d
    
def quadraticSolver(a,b,c):
    dis = b * b - 4 * a * c
    sqrt_val = math.sqrt(abs(dis))
    if dis > 0:
            print(" real and different roots ")
            print((-b + sqrt_val)/(2 * a))
            print((-b - sqrt_val)/(2 * a))
    elif dis == 0:
            print(" real and same roots")
            print(-b / (2 * a))
    else:
            print("Complex Roots")
            print(- b / (2 * a), " + i", sqrt_val)
            print(- b / (2 * a), " - i", sqrt_val)

def sequenceChecker(a, b, c, d, e):
    while 1 < 2:
        if b - a == c - b:
            print("Arithmetic")
            break
        if b / a == c / b or a / b == b / c:
            print("Geometric")
            break
        else:
            print("Quadratic")
            break
        
def nthFinder(a, b):
    a = str(a)
    b = str(b)
    x = a.replace("n", b)
    y = eval(x)
    return y
def nthRange(a, b, c):
    ls = []
    a = str(a)
    b = str(b)
    c = str(c)
    if int(b) > int(c):
        while int(c) < int(b)+1:
            x = a.replace("n", c)
            y = eval(x)
            ls.append(y)
            c = int(c)
            c=int(c)+1
            c = str(c)
    elif int(c) > int(b):
        while int(b) < int(c)+1:
            x = a.replace("n", b)
            y = eval(x)
            ls.append(y)
            b = int(b)
            b=int(b)+1
            b = str(b)
    return ls
def nthTable(a, b, c):
    ls = []
    a = str(a)
    b = str(b)
    c = str(c)
    if int(b) > int(c):
        while int(c) < int(b)+1:
            x = a.replace("n", c)
            y = eval(x)
            q = [c, y]
            ls.append(q)
            ls.append(q)
            c = int(c)
            c=int(c)+1
            c = str(c)
    elif int(c) > int(b):
        while int(b) < int(c)+1:
            x = a.replace("n", b)
            y = eval(x)
            q = [b, y]
            ls.append(q)
            b = int(b)
            b=int(b)+1
            b = str(b)
    headers = ["term", "value"]
    thing = tabulate(ls, headers = headers)
    print(thing)

def arithemeticSequence(term1, term2, term = 1):
    dif = term2 - term1
    before = term1 - dif
    newTerm = dif*term+before
    if before == 0:
        print("Nth Term:", str(dif) + "n")
        print(str(term) + "th term:", str(newTerm))
        
    else:
        if before < 0:
            print("Nth Term:", str(dif) + "n" + str(before))
            print(str(term) + "th term:", str(newTerm)) 
        else:
            print("Nth Term:", str(dif) + "n" + " + " + str(before))
            print(str(term) + "th term:", str(newTerm))  

def percentageChange(a, b):
    if a == b:
        return 100.0
    try:
        return round(((b - a)/a)*100, 3)
    except ZeroDivisionError:
        return float("inf")
def percentage(a, b, integer = False):
    percent = a / b * 100
    if integer:
        return int(percent)
    return percent

def average(*argv):
    total = np.sum(list(argv))
    length = len(argv)
    return total / length

def consecutiveIntCalc(x):
    a = (x/3)-1
    b = x/3
    c = (x/3)+1
    return [a, b, c]

def F(m, a):
    return m*a
def M(f, a):
    return f/a
def A(f, m):
    return f/m

def baseConverter(x, base):
    digs = string.digits + string.ascii_letters
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x = x // base

    if sign < 0:
        digits.append("-")

    digits.reverse()
    return "".join(digits)

def IntToBinary(num):
    return bin(num)[2:]
def BinaryToInt(num):
    return int(str(num), 2)
def IntToHexa(num):
    return hex(num)[2:]
def HexaToInt(num):
    return int(str(num, 2))
def binaryAdd(a, b):
    sum = BinaryToInt(a) + BinaryToInt(b)
    print("Binary:", IntToBinary(sum))
    print("Base 10:", sum)
def binarySubtract(a, b):
    sub = BinaryToInt(a) - BinaryToInt(b)
    print("Binary:", IntToBinary(sub))
    print("Base 10:", sub)
def binaryMultiply(a, b):
    mult = BinaryToInt(a) * BinaryToInt(b)
    print("Binary:", IntToBinary(mult))
    print("Base 10:", mult)
def binaryDivide(a, b):
    div = BinaryToInt(a) / BinaryToInt(b)
    print("Binary:", IntToBinary(div))
    print("Base 10:", div)
    
def hexaAdd(a, b):
    sum = HexaToInt(a) + HexaToInt(b)
    print("Hexadecimal:", IntToHexa(sum))
    print("Base 10:", sum)
def hexaSubtract(a, b):
    sub = HexaToInt(a) - HexaToInt(b)
    print("Hexadecimal:", IntToHexa(sub))
    print("Base 10:", sub)
def hexaMultiply(a, b):
    mult = HexaToInt(a) * HexaToInt(b)
    print("Hexadecimal:", IntToHexa(mult))
    print("Base 10:", mult)
def hexaDivide(a, b):
    div = HexaToInt(a) / HexaToInt(b)
    print("Hexadecimal:", IntToHexa(div))
    print("Base 10:", div)

def constSearch(con):
    G = 6.67384*10**(-11)
    c = 2.99792458*10**(8)
    h = 6.626070040*10**(-34)
    k = 1.38064852*10**(-23)
    F = 9.648533289*10**(4)
    pi = 3.141592653589793238462643
    e = 2.718281828459045235360287
    π = pi
    phi = 1.618033988749894848204586
    φ = phi
    conlist = [G, c, h, k, F, pi, π, φ, phi, e]
    x = 0
    while x < 10:
        variable_name = [k for k, v in locals().items() if v == conlist[x]][0]
        if variable_name == con:
            constant = conlist[x]
            return constant
        x += 1
    return None
def constTable():
    G = 6.67384*10**(-11)
    c = 2.99792458*10**(8)
    h = 6.626070040*10**(-34)
    k = 1.38064852*10**(-23)
    F = 9.648533289*10**(4)
    pi = 3.141592653589793238462643
    e = 2.718281828459045235360287
    π = pi
    phi = 1.618033988749894848204586
    φ = phi
    conlist = [["The gravitational constant", "G", G], ["The speed of light in vacuum", "c", c], ["Planck's constant", "h", h], ["Boltzmann's constant", "k", k], ["Faraday's constant", "F", F], ["e", "e", e], ["pi", "φ", π], ["Phi", "φ", φ]]
    headers = ["Name", "Symbol", "Value"]
    thing = tabulate(conlist, headers = headers)
    print(thing)


