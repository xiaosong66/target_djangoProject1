import datetime


def getMonth(now):
    year = now.year
    month = now.month
    day = now.day
    if month <= 2:
        year -= 1
        month = 12 + month - 2
    else:
        month -= 2

    # if month == 4:
    #     day = 28
    if month == 2:
        day = 28

    before = datetime.datetime(year, month, day)
    return before
