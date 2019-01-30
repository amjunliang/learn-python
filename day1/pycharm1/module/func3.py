def powerOf(num, power: int = 2):
    return num ** power


print(powerOf(*(3, 10)))
powerOf(num=3, power=4)


def fun(a, b, c="", d=""):
    pass


str = (
    "a"
    "b"
    "c"
)

print(str)

fun(100, "sf")

fun(100, 200, 100, 100)


def function_with_one_argument(a):
    print("test")
    pass


function_with_one_argument(100)


def tupledic(a, *t, **dic):
    print(a, t, dic)
    pass


dic = {"a": 100, "b": 300}
# tupledic(100, 29, b=3242, c=2343)
tupledic(**dic)

func = lambda a, b: a + b
print(func(100, 200))

pairs = [(4, 'one'), (3, 'two'), (2, 'three'), (1, 'four')]
pairs.sort(key=lambda a: a[0])
print(pairs)

print(__doc__)


def func():
    """  Documentation Strings.

    @see: https://docs.python.org/3/tutorial/controlflow.html#documentation-strings

    Here are some conventions about the content and formatting of documentation strings.
    The first line should always be a short, concise summary of the object’s purpose. For brevity,
    it should not explicitly state the object’s name or type, since these are available by other means
    (except if the name happens to be a verb describing a function’s operation). This line should begin
    with a capital letter and end with a period.

    If there are more lines in the documentation string, the second line should be blank, visually
    separating the summary from the rest of the description. The following lines should be one or more
    paragraphs describing the object’s calling conventions, its side effects, etc.

    """
    pass


print(func.__doc__)



