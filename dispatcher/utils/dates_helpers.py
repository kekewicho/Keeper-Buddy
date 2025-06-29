from datetime import datetime as dt

def next_paday_key():

    now = dt.now()

    return f"{now.year}-{now.month}-{1 if now.day <= 15 else 2}"