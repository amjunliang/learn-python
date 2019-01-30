try:
    result = 1 / 0
    print("")
#
except (ZeroDivisionError, NameError):
    print("ZeroDivisionError")
#
# except NameError:
#     print("a")
# except:
#     print("")
else:
    print("else")

# finally:
#     print("end")

print("test")


def func():
    raise ValueError("test")
    ValueError()


# func()

class Test:
    def func1(self):
        print(self)
        pass

    @classmethod
    def func2(cls):
        print(cls)
        pass

    @staticmethod
    def func3():
        print("func3")
        pass

    def func4():
        pass

    def __new__(cls, *args, **kwargs):
        # raise ValueError("test")
        return super().__new__(cls)


t = Test()
t.func1()
t.func2()
Test.func4()
t.func2()
t.func3()
Test.func1(t)

print("\n\nPerson:")


class Person(object, metaclass=type):
    """Silly Person"""

    def __new__(cls, name, age):
        print('__new__ called.')
        item = super(Person, cls).__new__(cls);
        item.name = name
        item.age = age
        return item

    def __init__(self, name, age):
        super(Person, self).__init__()
        print('__init__ called')
        # self.name = name
        # self.age = age

    def __str__(self):
        return '<Person: %s(%s)>' % (self.name, self.age)


print(Person("\n\nxiaoma", "10"))
print(hasattr(Person, "age"))


# print(Person("","").__metaclass__)


# the metaclass will automatically get passed the same argument
# that you usually pass to `type`
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """

    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attr = {}
    for name, val in future_class_attr.items():
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attr)


__metaclass__ = upper_attr  # this will affect all classes in the module


class Foo():  # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'


# print(hasattr(Foo, 'bar'))
# # Out: False
# print(hasattr(Foo, 'BAR'))
# # Out: True
#
# f = Foo()
# print(f.BAR)


# Out: 'bip'


# remember that `type` is actually a class like `str` and `int`
# so you can inherit from it
class UpperAttrMetaclass(type):
    # __new__ is the method called before __init__
    # it's the method that creates the object and returns it
    # while __init__ just initializes the object passed as parameter
    # you rarely use __new__, except when you want to control how the object
    # is created.
    # here the created object is the class, and we want to customize it
    # so we override __new__
    # you can do some stuff in __init__ too if you wish
    # some advanced use involves overriding __call__ as well, but we won't
    # see this
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return type(future_class_name, future_class_parents, uppercase_attr)


class UpperAttrMetaclass(type):

    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        # reuse the type.__new__ method
        # this is basic OOP, nothing magic in there
        return type.__new__(upperattr_metaclass, future_class_name,
                            future_class_parents, uppercase_attr)


class UpperAttrMetaclass(type):

    def __new__(cls, clsname, bases, dct):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return type.__new__(cls, clsname, bases, uppercase_attr)


class UpperAttrMetaclass(type):

    def __new__(cls, clsname, bases, dct):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)


# intercept a class creation
# modify the class
# return the modified class


class MEoor(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message

    pass


def func1():
    raise MEoor("test")


func1()
