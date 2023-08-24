import base64

with open("pebytes64_encode.txt", "r") as f:
    data = f.read()

decode_data = base64.b64decode(data)

with open("pebytes64_decode", "wb") as f:
    f.write(decode_data)