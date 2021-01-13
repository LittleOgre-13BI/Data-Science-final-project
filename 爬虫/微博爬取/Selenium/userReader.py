import re

def users():
    fw = open('userList.text','r')
    users = fw.readlines()

    userList = []

    for item in users:
        user = {}
        temp = item.split('<:>')
        user['name'] = temp[0]
        user['url'] = re.sub(r'\n','',temp[1])
        userList.append(user)

    return userList