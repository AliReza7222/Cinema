from cryptography.fernet import Fernet


def encode_data(data):
    data = str(data)
    key = Fernet.generate_key()
    obj_fernet = Fernet(key)
    encode = obj_fernet.encrypt(data.encode())
    string_encode = encode.decode('utf-8')

    return {'data-encode': string_encode, 'key': key}


def decode_data(data_encode, key):
    data_encode = data_encode.encode('utf-8')
    obj_fernet = Fernet(key)
    decode = obj_fernet.decrypt(data_encode).decode('utf-8')
    return eval(decode)
