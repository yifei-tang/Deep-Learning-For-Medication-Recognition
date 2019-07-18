import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
print(compare([1,2,3], [2.3,3]))
compare2([2,3],[3,4])