# Seed data

Generated using bcrypt python library

eg

```python
import bcrypt
password = b"alice123"
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
hashed = b"$2a$04$BOYcgGknfgS2yYAxtnXfEu6btv4bG8A1lE4UteDP7dU80TXW.Jmsa"
print(bcrypt.checkpw(password, hashed))
# True
```
