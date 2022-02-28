import re
def preprocessing(t):
    t_re = re.compile('\n+')
    t = t_re.sub('\n',t)
    return t
