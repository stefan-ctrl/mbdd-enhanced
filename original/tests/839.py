assert sort_tuple([("Amana", 28), ("Zenat", 30), ("Abhishek", 29),("Nikhil", 21), ("B", "C")]) == [('Abhishek', 29), ('Amana', 28), ('B', 'C'), ('Nikhil', 21), ('Zenat', 30)]
assert sort_tuple([("aaaa", 28), ("aa", 30), ("bab", 29), ("bb", 21), ("csa", "C")]) == [('aa', 30), ('aaaa', 28), ('bab', 29), ('bb', 21), ('csa', 'C')]
assert sort_tuple([("Sarala", 28), ("Ayesha", 30), ("Suman", 29),("Sai", 21), ("G", "H")]) == [('Ayesha', 30), ('G', 'H'), ('Sai', 21), ('Sarala', 28), ('Suman', 29)]
