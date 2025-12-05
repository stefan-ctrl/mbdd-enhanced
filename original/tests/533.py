assert remove_datatype((4, 5, 4, 7.7, 1.2), int) == [7.7, 1.2]
assert remove_datatype((7, 8, 9, "SR"), str) == [7, 8, 9]
assert remove_datatype((7, 1.1, 2, 2.2), float) == [7, 2]
