from hashlib import sha256

input_ = 'AAAAA'
print(sha256(input_.encode('utf-8')).hexdigest())