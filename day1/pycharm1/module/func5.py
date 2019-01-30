def logFunc(fun):
    print("logFunc")
    return lambda: print("test")


@logFunc
def func():
    print("func")


func()
