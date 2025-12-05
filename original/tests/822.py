assert pass_validity("password")==False
assert pass_validity("Password@10")==True
assert pass_validity("password@10")==False
