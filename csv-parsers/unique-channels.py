import csv
from collections import defaultdict

def count_unique_channels_per_author(file_path):
    # Dictionary to hold unique channels for each authorId
    channels_by_author = defaultdict(lambda: {'author_name': '', 'channels': set()})

    # Open and read the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV
        for row in reader:
            author_id = row['authorId']
            author_name = row['authorName']
            channel_name = row['channelName']

            # Add the channel to the set of channels for the given authorId
            channels_by_author[author_id]['author_name'] = author_name
            channels_by_author[author_id]['channels'].add(channel_name)

    # Return the results as a sorted list of tuples
    return sorted(
        [(author_id, data['author_name'], len(data['channels'])) for author_id, data in channels_by_author.items()],
        key=lambda x: (-x[2], x[0])  # Sort by number of unique channels (descending), then by authorId (ascending)
    )

# Usage example
file_path = '../csvs/input.csv'  # Replace with your CSV file path
author_channels = count_unique_channels_per_author(file_path)

# Print the results
for author_id, author_name, unique_channels in author_channels:
    print(f'Author ID: {author_id}, Author Name: {author_name}, Unique Channels: {unique_channels}')

