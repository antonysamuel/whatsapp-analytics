import pandas as pd
import re


def process_data(data):
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[a-z]{2}\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    df = pd.DataFrame()
    df['user_messages'] = messages[1:]
    df['message_date'] = dates
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    
    users = []
    messages = []
    for msg in df['user_messages']:
        entry = re.split('^(.*?):', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Whatsapp')
            messages.append(entry[0])
    
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['month'] = df.message_date.dt.month_name()
    df['day'] = df.message_date.dt.day
    df['year'] = df['message_date'].dt.year
    df['minute'] = df['message_date'].dt.minute
    df['hour'] = df['message_date'].dt.hour

    return df


if __name__ == '__main__':
    with open('chat.txt', 'r') as  chat:
        data = chat.read()
        df = process_file(data)
        print(df)