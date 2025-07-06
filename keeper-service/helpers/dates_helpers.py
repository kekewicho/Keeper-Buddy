from datetime import datetime as dt

def next_paday_key():

    now = dt.now()

    return f"{now.year}-{str(now.month).zfill(2)}-{1 if now.day <= 15 else 2}"