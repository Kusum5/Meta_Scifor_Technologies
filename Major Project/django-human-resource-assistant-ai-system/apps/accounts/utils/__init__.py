import shortuuid

GENDER =(("MASCULINO", "MASCULINE"),("FEMININO", "FEMININE"),)


def generate_otp(length=12):
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]

def generate_short_id(length=6):
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]

def deb():
    print("#"*100)
    print(f"{'Chamou': ^100}")
    print("#"*100)