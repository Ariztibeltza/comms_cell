from cryptography.fernet import Fernet

# Key creation
#key = Fernet.generate_key()
#print(key)

# Encryption
KEY = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='
fernet = Fernet(KEY)
f = open("rsrcs/permission.json","rb")
while(byte:=f.read(1)):
    encrypted_f = fernet.encrypt(byte)
