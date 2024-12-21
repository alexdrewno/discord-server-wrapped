import csv
from collections import defaultdict

def count_messages_in_anime_channel(file_path):
    # Dictionary to hold the message count for each authorId and authorName
    messages_by_author = defaultdict(lambda: {'author_name': '', 'message_count': 0})

    # Open and read the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV
        for row in reader:
            channel_name = row['channelName']
            if channel_name.lower() == 'anime':  # Only consider rows where the channel is 'anime'
                author_id = row['authorId']
                author_name = row['authorName']

                # Increment the message count for this authorId
                messages_by_author[author_id]['author_name'] = author_name
                messages_by_author[author_id]['message_count'] += 1

    # Return the results as a sorted list of tuples
    return sorted(
        [(author_id, data['author_name'], data['message_count']) for author_id, data in messages_by_author.items()],
        key=lambda x: (-x[2], x[0])  # Sort by message count (descending), then by author_id (ascending)
    )

# Usage example
file_path = '../csvs/input.csv'  # Replace with your CSV file path
author_messages = count_messages_in_anime_channel(file_path)

# Print the results
for author_id, author_name, message_count in author_messages:
    print(f'Author ID: {author_id}, Author Name: {author_name}, Messages in Anime Channel: {message_count}')

