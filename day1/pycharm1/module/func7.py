import random


def funYield():
    for i in range(3):
        yield random.randint(1, 10)
    yield random.randint(10, 20)


#
# obj = funYield()
#
# print(obj.__next__())
# print(obj.__next__())
# print(obj.__next__())
# print(obj.__next__())
# print(obj.__next__())

for a in funYield():
    print(a)

for number_index, random_number in enumerate(funYield()):
    if number_index < 3:
        assert 0 <= random_number <= 10
    else:
        assert 10 <= random_number <= 20
#
# str1: list = "test"
# str1.append("a")
# print(str1)

str1: str = ""

if str1:
    print(str1)
else:
    print("nil")

print(bool(str1))
