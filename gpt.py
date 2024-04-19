list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]

# 将列表转换为元组
set1 = set(tuple(list1))
set2 = set(tuple(list2))

# 使用集合的交集操作符（&）找到交集
intersection = set1 & set2

print(intersection)
