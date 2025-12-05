assert remove_char("123abcjw:, .@! eiw") == '123abcjweiw'
assert remove_char("Hello1234:, ! Howare33u") == 'Hello1234Howare33u'
assert remove_char("Cool543Triks@:, Make@987Trips") == 'Cool543TriksMake987Trips' 
