from io import TextIOWrapper
from datetime import datetime, date
import re

def parse_date(date_str: str) -> date | None:
    """
    Parses a date string in 'YYYY-MM-DD' or 'DD-MM-YYYY' format into a date object.
    """
    formats = ["%Y-%m-%d", "%d-%m-%Y"]  # Accepted formats
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue  # Try next format if parsing fails
    return None


class Vouchar:
    DOWNPAYMENT = 'downpayment'
    COLLECTION = 'collection'
    
    @staticmethod
    def is_downpayment(vouchar: str) -> bool:
        # Check if voucher matches the 'downpayment' format
        return True if re.match(r'^[A-Z]{3}-HF\d+$', vouchar) else False
    
    @staticmethod
    def is_collection(vouchar: str) -> bool:
        # Check if voucher matches the 'collection' format
        return True if re.match(r'^[A-Z]{3}-HC\d+$', vouchar) else False
    
    @staticmethod
    def vouchar_type(vouchar: str) -> str | None:
        # Check if voucher matches the 'collection' format
        if re.match(r'^[A-Z]{3}-HC\d+$', vouchar):
            return Vouchar.COLLECTION

        # Check if voucher matches the 'downpayment' format
        if re.match(r'^[A-Z]{3}-HF\d+$', vouchar):
            return Vouchar.DOWNPAYMENT
        
        return None
        

def read_bcb_file(uploaded_file, date=None) -> list | list[dict]:
    """
    Read a UTF-16 encoded tab-separated .xls file uploaded via Django
    and return selected columns as a 2D list.
    """
    data = []
    if not uploaded_file or not uploaded_file.name.endswith('.xls'):
        return data

    # Index of columns in the .xls file
    columns = {
        'account': 4, 
        'receipt_id': 7, 
        'amount': 12, 
        'date': 18
    }

    # Provided .xls file is in utf-16, so Wrap the file in a UTF-16 decoder
    text_stream = TextIOWrapper(uploaded_file.file, encoding='utf-16')

    for line in text_stream:
        row = line.strip().split('\t')
        
        if not max(columns.values()) < len(row):
            continue
        
        selected = {}
        for key, val in columns.items():
            selected[key] = row[val].strip()
            
        try: # fix amount 1,200.00 -> 1200
            amount = str(selected['amount'])
            selected['amount'] = int(float(amount.replace(',', '')))
        except Exception:
            pass
        
        # append only down payment or collection
        vouchar = Vouchar.vouchar_type(selected['receipt_id'])
        if vouchar:
            selected['type'] = vouchar
            data.append(selected)
        
    given_date = parse_date(date) if date else None
    if given_date:
        return [
            row for row in data 
            if parse_date(row['date']) == given_date
        ]
    return data
    