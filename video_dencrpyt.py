from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64decode

def decrypt_m3u8_url(encrypted_url, newSign):
    try:
        key = newSign[4:20]  # "1234567890123456" from the substring of newSign
        iv = "b1da7878016e4e2b"  # Hardcoded IV
        # Decode the base64 encoded encrypted URL
        encrypted_data = b64decode(encrypted_url)

        # Convert the key and IV into byte arrays
        parsed_key = key.encode('utf-8')
        parsed_iv = iv.encode('utf-8')

        # Create the AES cipher object
        cipher = Cipher(algorithms.AES(parsed_key), modes.CBC(parsed_iv))

        # Decrypt the data
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(128).unpadder()  # 128-bit block size for AES
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        # Convert the decrypted data to string (assuming UTF-8 encoding)
        return unpadded_data.decode('utf-8')

    except Exception as e:
        print("Decryption failed:", e)
        return ""

