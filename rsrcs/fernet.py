from cryptography.fernet import Fernet

# Key creation
#key = Fernet.generate_key()
#print(key)

# Encryption
KEY = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='
fernet = Fernet(KEY)
f = open("rsrcs/permission.json","rb")
f_enc = open("rsrcs/enc.json","wb")
f_dec = open("rsrcs/denc.json","wb")

original = f.read()
encrypted = fernet.encrypt(original)
f_enc.write(encrypted)
f_dec.write(fernet.decrypt(encrypted))
# Encripting bytes
#while(byte:=f.read(1)):
#    enc_byte = fernet.encrypt(byte)
#    f_enc.write(enc_byte)

f.close()
f_enc.close()
