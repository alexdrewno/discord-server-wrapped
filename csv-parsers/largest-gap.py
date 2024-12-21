import csv
from collections import defaultdict
from datetime import datetime, timedelta

def find_top_10_largest_gaps(file_path):
    # Dictionary to hold the list of message times for each authorId
    messages_by_author = defaultdict(list)

    # Open and read the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV
        for row in reader:
            author_id = row['authorId']
            author_name = row['authorName']
            message_date_str = row['messageDate']
            bot_status = row['bot'].lower() == 'true'  # Convert to boolean (True if bot column is 'true')

            # Skip bot messages
            if bot_status:
                continue

            # Convert messageDate string to datetime object
            try:
                message_date_str = message_date_str.split('.')[0]
                message_date = datetime.strptime(message_date_str, '%Y-%m-%d %H:%M:%S')  # Adjust the format if needed
            except ValueError:
                continue  # Skip invalid datetime formats

            # Append the message datetime for this authorId
            messages_by_author[author_id].append((author_name, message_date))

    # List to hold the author_id, author_name, and the largest gap
    author_gaps = []

    # Calculate the largest gap for each author
    for author_id, messages in messages_by_author.items():
        # Sort messages by datetime
        messages.sort(key=lambda x: x[1])  # Sorting by message_date

        largest_gap = timedelta(seconds=0)  # Start with a 0 gap
        # Calculate gaps between consecutive messages
        for i in range(1, len(messages)):
            prev_message_time = messages[i - 1][1]
            current_message_time = messages[i][1]
            gap = current_message_time - prev_message_time

            # Update largest gap for this author
            if gap > largest_gap:
                largest_gap = gap

        # Store author_id, author_name, and largest_gap
        author_gaps.append((author_id, messages[0][0], largest_gap))  # messages[0][0] gives author_name

    # Sort the authors by largest gap (descending) and pick top 10
    top_10_authors = sorted(author_gaps, key=lambda x: x[2], reverse=True)[:10]

    return top_10_authors

# Usage example
file_path = '../csvs/input.csv'  # Replace with your CSV file path
top_10_authors = find_top_10_largest_gaps(file_path)

# Print the results
print("Top 10 Authors with the Largest Gap Between Messages (excluding bots):")
for author_id, author_name, gap in top_10_authors:
    print(f"Author ID: {author_id}, Author Name: {author_name}, Largest Gap: {gap}")

