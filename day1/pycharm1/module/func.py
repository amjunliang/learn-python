def fibonacci_function_example(nuber_limit):
    """
    文档说明
    :return:
    """
    fibonacci_list = []
    previous_number, current_number = 0, 1
    while previous_number < nuber_limit:
        fibonacci_list.append(previous_number)
        previous_number, current_number = current_number, previous_number + current_number

    return fibonacci_list


def closure(name):
    def message():
        return "hello" + name

    return message


def test_a():
    print(fibonacci_function_example(20))
    print(closure('xiaoma')())
    pass



def test_b():
    print(fibonacci_function_example(20))
    print(closure('xiaoma')())
    pass
