#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.basic_auth import BasicAuth

    ba = BasicAuth()
    res1, res2 = ba.extract_user_credentials("Holberton")
    if res1 is not None:
        print("extract_user_credentials must return None, None if 'decoded_base64_authorization_header' doesn't contain ':'")
        exit(1)
    if res2 is not None:
        print("extract_user_credentials must return None, None if 'decoded_base64_authorization_header' doesn't contain ':'")
        exit(1)
    
    print("OK", end="")
