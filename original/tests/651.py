assert check_subset((10, 4, 5, 6), (5, 10)) == True
assert check_subset((1, 2, 3, 4), (5, 6)) == False
assert check_subset((7, 8, 9, 10), (10, 8)) == True
