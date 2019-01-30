import re

print(re.search(r"py", "pypython, python", re.M))
print(re.match(r'^(\d+?)(0*)$', '102300').groups())
