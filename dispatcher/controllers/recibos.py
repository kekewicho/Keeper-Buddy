from utils.dates_helpers import next_paday_key

def add_paid_bills(bill_name:str, amount: float, payday: str = None):

    payday_key = payday or next_paday_key()
