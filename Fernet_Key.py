from cryptography.fernet import Fernet


# Fernet encryption/decryption example with encrypting in one session and then using a different session
# To decrypt file with Fernet asymmetric key
# Comment out decryption and run encryption
# Then uncomment decryption and comment out encryption and key generation and decrypt file

# key = Fernet.generate_key()
# print(key)
# cryptor = Fernet(key)

# with open('fernet_key.txt', 'wb') as f:
#     f.write(key)

# with open('anonymous.jpg', 'rb') as f:
#     data = f.read()
#     with open('enc_pic.jpg', 'wb') as f:
#         crypt_data = cryptor.encrypt(data)
#         f.write(crypt_data)
#     print('Encrypted')


with open('fernet_key.txt', 'r') as f:
    key = f.read()
cryptor = Fernet(key)

with open('enc_pic.jpg', 'rb') as f:
    data = f.read()
with open('dec_pic.jpg', 'wb') as f:
    decrypt_data = cryptor.decrypt(data)
    f.write(decrypt_data)
    print('Decrypted!')