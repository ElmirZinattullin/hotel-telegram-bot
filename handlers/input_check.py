import datetime

def valid_input_date(text_message):
    check_in_date_list = text_message.split('/')
    today = datetime.date.today()
    current_year = today.year
    if len(check_in_date_list) == 2:
        try:
            check_in_date = datetime.date(current_year, int(check_in_date_list[1]), int(check_in_date_list[0]))
            if check_in_date < today:
                check_in_date = datetime.date(current_year + 1, int(check_in_date_list[1]), int(check_in_date_list[0]))
        except:
            return None
    else:
        return None
    return check_in_date

