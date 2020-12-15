import codecs

look = codecs.lookup(' gb2312 ')

look2 = codecs.lookup(' utf-8 ')

a = ' 我爱北京 '

# print(len(a),a)

b = look.decode(a.encode('gb2312'))

# print(b[1],b[0],type(b[0]))

b2 = look.encode(b[0])

print(b2[1],b2[0],type(b2[0]))
#
# print(len(b2[0]))