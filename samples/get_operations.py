from creditagricole_particuliers import Authenticator, Accounts

session = Authenticator(username="0000000000001", password=[1, 2, 3, 4, 5, 6], department=999)

# search account
account = Accounts(session=session).search(num="0000000000001")

# get operations
operations = account.get_operations(count=30)
for op in operations:
    print(op)
