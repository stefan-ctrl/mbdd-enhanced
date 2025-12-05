assert concatenate_nested((3, 4), (5, 6)) == (3, 4, 5, 6)
assert concatenate_nested((1, 2), (3, 4)) == (1, 2, 3, 4)
assert concatenate_nested((4, 5), (6, 8)) == (4, 5, 6, 8)
