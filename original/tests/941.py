assert count_elim([10,20,30,(10,20),40])==3
assert count_elim([10,(20,30),(10,20),40])==1
assert count_elim([(10,(20,30,(10,20),40))])==0
