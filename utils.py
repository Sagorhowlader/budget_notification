import datetime


def get_current_month_date() -> str:
    """Gets the current month and year in the format "YYYY-MM-DD".

    Returns:
        The current month and year as a string in the format "YYYY-MM-DD".
    """
    now = datetime.date.today().replace(day=1)  # return current month first date.
    date = now.strftime('%Y-%m-%d')
    return date
