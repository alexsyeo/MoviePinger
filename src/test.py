import json

# try:
with open('src/test.txt') as json_file:
    data = json.load(json_file)
    print('inside')
    if (data):
        print('yes')
    else:
        print('no')
# except:
#     print("an exception has occurred")