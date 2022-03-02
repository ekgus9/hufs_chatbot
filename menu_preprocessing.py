import re
def preprocessing(t):
    t_re = re.compile('\n{3,}')
    t = t_re.sub('\n\n',t)
    return t
