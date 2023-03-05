import re

with open('chat1.txt', 'r') as file1:
    file_str = file1.read()
    file_str = re.sub(r'[^a-zA-Z0-9\s]', '', file_str)