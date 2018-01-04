import bcrypt
password = b"-ankVuPqceD(LBd0Zc"
hashed = b"$2a$04$BOYcgGknfgS2yYAxtnXfEu6btv4bG8A1lE4UteDP7dU80TXW.Jmsa"
print(bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a")))
print(bcrypt.checkpw(password, hashed))
