assert group_keyvalue([('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)])=={'yellow': [1, 3], 'blue': [2, 4], 'red': [1]}
assert group_keyvalue([('python', 1), ('python', 2), ('python', 3), ('python', 4), ('python', 5)])=={'python': [1,2,3,4,5]}
assert group_keyvalue([('yellow',100), ('blue', 200), ('yellow', 300), ('blue', 400), ('red', 100)])=={'yellow': [100, 300], 'blue': [200, 400], 'red': [100]}
