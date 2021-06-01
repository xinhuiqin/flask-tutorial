class A(object):
    bar = 1

    def hello(self):
        print('hello')


a = A()
res = getattr(a, 'hello')
print(res)
