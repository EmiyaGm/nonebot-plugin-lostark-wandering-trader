import datetime

def get_display_at():
    now = datetime.datetime.now()
    hour = now.hour
    date = datetime.datetime.now().date().isoformat()
    show_time_array = [datetime.datetime.strptime( date + ' ' + '04:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '10:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '16:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '22:00:00', '%Y-%m-%d %H:%M:%S'),]

    display_at = None

    if hour >= 4 and hour <= 9:
        display_at = show_time_array[0]
        
    if hour >= 10 and hour <= 15:
        if hour == 15:
            minute = now.minute
            if minute >= 30:
                display_at = None
            else:
                display_at = show_time_array[1]
        else:
            display_at = show_time_array[1]
            
    if hour >= 16 and hour <= 21:
        if hour == 21:
            minute = now.minute
            if minute >= 30:
                display_at = None
            else:
                display_at = show_time_array[2]
        else:
            display_at = show_time_array[2]
        
    if hour >= 22:
        display_at = show_time_array[3]

    if hour <= 3:
        if hour == 3:
            minute = now.minute
            if minute >= 30:
                display_at = None
            else:
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                display_at = datetime.datetime.strptime(yesterday.isoformat() + '22:00:00', '%Y-%m-%d %H:%M:%S')
        else:
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            display_at = datetime.datetime.strptime(yesterday.isoformat() + '22:00:00', '%Y-%m-%d %H:%M:%S')
    
    return display_at