import jsonspot
x={'a':1,'b':{'b1':2}}
expect=2
x=jsonspot.is_expect('{"a":1}',expect)
print(x)