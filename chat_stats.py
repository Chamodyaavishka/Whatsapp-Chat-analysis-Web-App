import pandas as pd
import imoji
import re

def fetch_stats(chat_file):
    with open(chat_file, 'r', encoding="utf8") as file:
        lines = file.readlines()

    pattern = '(\d{1,2}\/\d{1,2}\/\d{2,4}, \d{1,2}:\d{2}) - (.*?): (.*)'
    chat = []
    for line in lines:
        match = re.search(pattern, line)
        if match:
            date = match.group(1)
            sender = match.group(2)
            message = match.group(3)

            # Remove any emojis and other non-word characters from message
            message = re.sub(emoji.get_emoji_regexp(), r'', message)
            message = re.sub(r'[^\w\s]', '', message)

            chat.append((date, sender, message))

    df = pd.DataFrame(chat, columns=['date', 'sender', 'message'])
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p')
    df = df.set_index('date')

    stats = {
        'Total Messages': len(df),
        'Total Words': df['message'].apply(lambda x: len(x.split())).sum(),
        'Total Characters': df['message'].apply(len).sum(),
        'Average Message Length': df['message'].apply(len).mean(),
        'Most Active': df['sender'].value_counts().index[0],
        'Total Emojis': sum(df['message'].apply(emoji.emojize).apply(emoji_count)),
    }

    return stats

def imoji_count(text):
    return len([c for c in text if c in imoji.UNICODE_IMOJI['en']])
