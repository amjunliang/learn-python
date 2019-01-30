def fun(a: str, b: int = 100) -> str:
    '''
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)


    :param a:
    :param b:
    :return:
    '''

    def greeting(name):
        return "Hello, {0}!".format(name)

    def decorate_with_p(func):
        def function_wrapper(name):
            return "<p>{0}</p>".format(func(name))

        return function_wrapper

    print(a, b)


print(fun.__annotations__)

