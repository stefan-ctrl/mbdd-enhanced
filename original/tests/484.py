assert remove_matching_tuple([('Hello', 'dude'), ('How', 'are'), ('you', '?')], [('Hello', 'dude'), ('How', 'are')]) == [('you', '?')]
assert remove_matching_tuple([('Part', 'of'), ('the', 'journey'), ('is ', 'end')], [('Journey', 'the'), ('is', 'end')]) == [('Part', 'of'), ('the', 'journey'), ('is ', 'end')]
assert remove_matching_tuple([('Its', 'been'), ('a', 'long'), ('day', 'without')], [('a', 'long'), ('my', 'friend')]) == [('Its', 'been'), ('day', 'without')]
