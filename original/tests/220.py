assert replace_max_specialchar('Python language, Programming language.',2)==('Python:language: Programming language.')
assert replace_max_specialchar('a b c,d e f',3)==('a:b:c:d e f')
assert replace_max_specialchar('ram reshma,ram rahim',1)==('ram:reshma,ram rahim')
