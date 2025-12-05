assert check_identical([(10, 4), (2, 5)], [(10, 4), (2, 5)]) == True
assert check_identical([(1, 2), (3, 7)], [(12, 14), (12, 45)]) == False
assert check_identical([(2, 14), (12, 25)], [(2, 14), (12, 25)]) == True
