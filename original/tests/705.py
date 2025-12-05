assert sort_sublists([[2], [0], [1, 3], [0, 7], [9, 11], [13, 15, 17]])==[[0], [2], [0, 7], [1, 3], [9, 11], [13, 15, 17]]
assert sort_sublists([[1], [2, 3], [4, 5, 6], [7], [10, 11]])==[[1], [7], [2, 3], [10, 11], [4, 5, 6]]
assert sort_sublists([["python"],["java","C","C++"],["DBMS"],["SQL","HTML"]])==[['DBMS'], ['python'], ['SQL', 'HTML'], ['java', 'C', 'C++']]
