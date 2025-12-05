assert remove_empty([(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')])==[('',), ('a', 'b'), ('a', 'b', 'c'), 'd']  
assert remove_empty([(), (), ('',), ("python"), ("program")])==[('',), ("python"), ("program")]  
assert remove_empty([(), (), ('',), ("java")])==[('',),("java") ]  
