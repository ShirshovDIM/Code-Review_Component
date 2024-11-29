import os,sys,math
def testFunc(a,b,c):
    return a+b*c- (b+a/4)+math.sqrt(b)
x = 12; y = 3; z= 8
if(x>y):
    print('x > y')
else:
    print('x <= y')
if x!=z :
    print("x != z"); 
def anotherFunc(val1,Val2):
    return val1 +Val2
class myclass:
    def __init__(self,arg1,arg2):
        self.arg1=arg1;
        self.arg2=arg2
    def display(self):
        print("Values",self.arg1,self.arg2)
obj = myclass(1,2)
obj.display()
