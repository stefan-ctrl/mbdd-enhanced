assert remove_words(['red', 'green', 'blue', 'white', 'black', 'orange'],['white', 'orange'])==['red', 'green', 'blue', 'black']
assert remove_words(['red', 'green', 'blue', 'white', 'black', 'orange'],['black', 'orange'])==['red', 'green', 'blue', 'white']
assert remove_words(['red', 'green', 'blue', 'white', 'black', 'orange'],['blue', 'white'])==['red', 'green', 'black', 'orange']
