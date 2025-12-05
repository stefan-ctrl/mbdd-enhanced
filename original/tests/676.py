assert remove_extra_char('**//Google Android// - 12. ') == 'GoogleAndroid12'
assert remove_extra_char('****//Google Flutter//*** - 36. ') == 'GoogleFlutter36'
assert remove_extra_char('**//Google Firebase// - 478. ') == 'GoogleFirebase478'
