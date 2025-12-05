assert extract_min_max((5, 20, 3, 7, 6, 8), 2) == (3, 5, 8, 20)
assert extract_min_max((4, 5, 6, 1, 2, 7), 3) == (1, 2, 4, 5, 6, 7)
assert extract_min_max((2, 3, 4, 8, 9, 11, 7), 4) == (2, 3, 4, 7, 8, 9, 11)
