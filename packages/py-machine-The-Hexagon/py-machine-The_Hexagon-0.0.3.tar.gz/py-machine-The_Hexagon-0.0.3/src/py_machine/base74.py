int_decode = enumerate(
  "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^}{"
)

encode_int = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^}{"

def b74intdecode(text):
    num = 0
    text = list(text[::-1])
    for i in range(len(text)):
        temp_num = int_decode[text[i]]
        num += temp_num * 74**i
    return num

def b74intencode(text):
    if text < 74:
        return encode_int[text]
    else:
        return b74intencode(text // 74) + encode_int[text % 74]