test = '<<users>><user><id><1></id><name>Ahmed Ali </name></user></users>'
open = []
tokens = []
expected_tokens = ['users', 'user', 'id', 'name', 'posts', 'post', 'followers', 'follower', 'topics', 'topic','body']
indexes = []
temp = ''
flag = False

for index, item in enumerate(test):
    if item == '<':
        open.append(item)
        indexes.append(index)
        if temp not in expected_tokens:
            temp = ''

    elif item == '>':
        if flag and temp in expected_tokens:
            if temp != tokens[-1]:
                print(f'Error in index{index - len(temp)}')
            else:
                tokens.pop()
                temp = ''
            flag = False

        if open:
            open.pop()
            indexes.pop()
        else:
            print(f'Error in  index{index}')

        if temp != '' and temp in expected_tokens:
            tokens.append(temp)
            temp = ''


    elif item == '/':
        flag = True
    else:
        temp = temp + item
    # print(tokens)
    # print(temp)
    # print(open)

if indexes:
    # for index  in indexes:
    indexes_error = ','.join(indexes)
    print(f'Errors in indexes {indexes_error}')
for token in tokens:
    print(token)
