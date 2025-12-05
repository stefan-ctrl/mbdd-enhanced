assert check_IP("192.168.0.1") == 'Valid IP address'
assert check_IP("110.234.52.124") == 'Valid IP address'
assert check_IP("366.1.2.2") == 'Invalid IP address'
