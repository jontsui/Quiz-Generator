import re


s = '1 + sqrt((x+3)/(x-3))'

x = re.split('([()/*+])', s)

x = [token for token in x if token]

print(x)







