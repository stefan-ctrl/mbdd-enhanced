assert remove_words(['Red color', 'Orange#', 'Green', 'Orange @', "White"],['#', 'color', '@'])==['Red', '', 'Green', 'Orange', 'White']
assert remove_words(['Red &', 'Orange+', 'Green', 'Orange @', 'White'],['&', '+', '@'])==['Red', '', 'Green', 'Orange', 'White']
assert remove_words(['Red &', 'Orange+', 'Green', 'Orange @', 'White'],['@'])==['Red &', 'Orange+', 'Green', 'Orange', 'White']
