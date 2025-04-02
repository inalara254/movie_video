import hmac
import hashlib
import base64
import time
import requests
import json
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from six import print_
from video_dencrpyt import decrypt_m3u8_url
import urllib.parse


def sort_url_params(url_with_params):
    # Split the URL into its base and query parts
    parsed_url = urllib.parse.urlparse(url_with_params)

    # Extract the query parameters
    params = urllib.parse.parse_qs(parsed_url.query)

    # Sort the parameters by their key names
    sorted_params = sorted(params.items())

    # Rebuild the query string from the sorted parameters
    sorted_query_string = urllib.parse.urlencode(sorted_params, doseq=True)

    # Reconstruct the full URL with sorted parameters
    base_url = parsed_url.path
    full_url = f"{base_url}?{sorted_query_string}" if sorted_query_string else base_url

    return full_url


def decrypt_base64_aes_ecb(data_b64, key):
    data = base64.b64decode(data_b64)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()

    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

def send_request(url):
    secret = "ES513W0B1CsdUrR13Qk5EgDAKPeeKZY"
    timestamp = str(int(time.time() * 1000))
    url=sort_url_params(url)
    params = f"GET\naliId:kym8R81Uy1hoFX6vI3717k8awp3X\nct:web_pc\ncv:1.0.0\nt:{timestamp}\n{url}"
    # Generate the HMAC-SHA256 signature
    signature = hmac.new(
        secret.encode(),
        msg=params.encode(),
        digestmod=hashlib.sha256
    ).digest()

    # Base64 encode the signature
    signature_base64 = base64.b64encode(signature).decode()
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "aliid": "kym8R81Uy1hoFX6vI3717k8awp3X",
        "clienttype": "web_pc",
        "clientversion": "1.0.0",
        "connection": "keep-alive",
        "ct": "web_pc",
        "cv": "1.0.0",
        "deviceid": "kym8R81Uy1hoFX6vI3717k8awp3X",
        "host": "api.rrmj.plus",
        "origin": "https://m.rrmj.plus",
        "referer": "https://m.rrmj.plus/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "t": timestamp,
        "token": "",
        "Uet":"9",
        "umid": "kym8R81Uy1hoFX6vI3717k8awp3X",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-ca-sign": signature_base64
    }
    # Construct the params string based on the provided URL and timestamp

    request_url = "https://api.rrmj.plus"+url

    # Make the GET request
    response = requests.get(request_url, headers=headers)
    #decrypt
    key = b"3b744389882a4067"
    decrypted_text = decrypt_base64_aes_ecb(response.text, key)
    json_data = json.loads(decrypted_text)

    # decrypt the url of the video if it exists
    if  json_data.get("data", {}).get("watchInfo", {}).get("m3u8", {}).get("url"):
        video_url=json_data["data"]["watchInfo"]["m3u8"]["url"].strip()
        newsign=json_data["data"]["newSign"].strip()
        video_decrptied=decrypt_m3u8_url(video_url,newsign)
        json_data["data"]["watchInfo"]["m3u8"]["url"]=video_decrptied
    return json_data

# Example usage

