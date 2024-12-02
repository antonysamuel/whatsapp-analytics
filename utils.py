import pandas as pd
import re
from urlextract import URLExtract
extract = URLExtract()

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


def fetch_stats(df, user):
    
    if user != 'Overall':
        df = df[df['users'] == user]

    messages = df.messages
    num_messages = messages.shape[0]
    num_media_shared = df[df.messages == ' <Media omitted>\n'].shape[0]
    words = []
    for message in messages:
        if message != ' <Media omitted>\n':
            words.extend(message.split())

    num_words = len(words)

    urls = []
    for message in messages:
        urls.extend(extract.find_urls(message))
    num_urls = len(urls)

    return num_messages, num_words, num_media_shared, num_urls


if __name__ == '__main__':
    with open('chat.txt', 'r') as  chat:
        data = chat.read()
        df = process_file(data)
        print(df)