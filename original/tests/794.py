assert text_starta_endb("aabbbb")==('Found a match!')
assert text_starta_endb("aabAbbbc")==('Not matched!')
assert text_starta_endb("accddbbjjj")==('Not matched!')
