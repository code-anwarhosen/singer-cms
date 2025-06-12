from io import TextIOWrapper
from datetime import datetime, date


def parse_date(date_str: str) -> date | None:
    """
    Parses a date string in 'YYYY-MM-DD' or 'DD-MM-YYYY' format into a date object.
    """
    
    formats = ["%Y-%m-%d", "%d-%m-%Y"]  # Accepted formats

    for fmt in formats:
        try:
            # Parse into datetime, then convert to date
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue  # Try next format if parsing fails

    # None of the formats matched
    return None


def read_bcb_file(uploaded_file, date=None) -> list:
    """
    Read a UTF-16 encoded tab-separated .xls file uploaded via Django
    and return selected columns as a 2D list.
    """
    
    if not uploaded_file.name.endswith('.xls'):
        return []

    # hire account, receipt, amount, date
    columns = [4, 7, 12, 18]
    data = []
    
    given_date = parse_date(date) if date else None

    # Wrap the uploaded file in a UTF-16 decoder
    text_stream = TextIOWrapper(uploaded_file.file, encoding='utf-16')

    for line in text_stream:
        row = line.strip().split('\t')
        if not max(columns) < len(row):
            continue

        selected = [row[col].strip() for col in columns]
        
        # append only if it is down payment or collection
        # if first item is empty, then it is not down payment or collection
        if selected and selected[0]:
            data.append(selected)
    
    # remove title (first) column
    if data and data[0]:
        del data[0]
        
    given_date = parse_date(date) if date else None
    if given_date:
        return [
            row for row in data 
            if parse_date(row[-1]) == given_date
        ]
    
    return data  # List of selected columns per row
    