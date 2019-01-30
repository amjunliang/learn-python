# class A:
#     """
#     docs
#     """
#     name = "test"
#     _score = "abc"
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
#
#     def __init__(self, name=""):
#         self.name = name
#         self._score = ""
#
#     def func1(self):
#         self.name = "func1"
#         print(self.name)
#
#     def func2(self):
#         print("func2")
#
#     def get_name(self):
#         return self.name
#
#
# a = A()
# # a.func1()
# # a.func2()
# a.func2()
# A.func2(a)
# print(a.get_name())
# A.func2("")
# print(a.name)
# a.test = "abcde"
# print(a.test)
# A.sex = "sex"
#
# a = A()
# a.sex = "abc"
# print(a.sex)
#
# print(A.__doc__)

# A("")
# a = A()
# a.score = "100"
# print("a", a.score)


class ClassA():
    a = "10"
    b = "20"
    _name = 'protected类型的变量'
    __info = '私有类型的变量'

    def _func(self):
        print("这是一个protected类型的方法")

    def __func2(self):
        print('这是一个私有类型的方法')

    def get(self):
        return (self.__info)


a = ClassA()
a.a = "10"
a.b = "20"
# print(dir(a))
# print(a.get())
print(a.__doc__)
print(a.__dict__)
print(a.__module__)
# print(a.__bases__)ases : 类的所有父类构成元素（包含了一个由所有父类组成的元组）

# a.__func2()
# print(a.__info)
a._func()
# print(A._name)
print(a._name)


# print(ClassA.__info)


# print(a.abc)
# a._name()

class Person:
    """Example of the base class"""


def __init__(self, name):
    self.name = name


def get_name(self):
    """Get person name"""
    return self.name


class Employee(Person):
    """Example of the derived class

    """

    def __init__(self, name, staff_id):
        super.__init__(name)
        Person.__init__(self, name)
        # You may also use super() here in order to avoid explicit using of parent class name:
        # >>> super().__init__(name)
        self.staff_id = staff_id

    def get_full_id(self):
        """Get full employee id"""
        return self.get_name() + ', ' + self.staff_id
