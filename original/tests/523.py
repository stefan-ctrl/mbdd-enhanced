assert check_string('python')==['String must have 1 upper case character.', 'String must have 1 number.', 'String length should be atleast 8.']
assert check_string('123python')==['String must have 1 upper case character.']
assert check_string('123Python')==['Valid string.']
