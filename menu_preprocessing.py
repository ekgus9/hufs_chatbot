import re
def preprocessing(t):
    t_re = re.compile('[0-9],[0-9]+원')
    t = t_re.sub('',t)
    t_re = re.compile('[0-9]+ Kcal')
    t = t_re.sub('',t)
    t = t.split('\n')
    t = [i for i in t if (':' not in i) and ('~' not in i) and ('' != i)]
    return '\n'.join(t)