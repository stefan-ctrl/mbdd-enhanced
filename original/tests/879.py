assert text_match("aabbbbd") == 'Not matched!'
assert text_match("aabAbbbc") == 'Not matched!'
assert text_match("accddbbjjjb") == 'Found a match!'
