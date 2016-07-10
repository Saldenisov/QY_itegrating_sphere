try:
    a  = 2
    raise FileNotFoundError
except FileNotFoundError as e:
    print(e)