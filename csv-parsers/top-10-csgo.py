import csv
from collections import Counter

def get_top_users_in_channel(csv_file, channel_name='counter-strike', top_n=10):
    # Dictionary to store message count per user
    user_message_count = Counter()

    # Open and read the CSV file
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV
        for row in reader:
            # Only consider messages from the 'counter-strike' channel
            if row['channelName'] == channel_name:
                user_message_count[row['authorName']] += 1
    
    # Get the top N users sorted by message count (descending)
    top_users = user_message_count.most_common(top_n)
    
    # Format the results
    result = []
    for i, (user, message_count) in enumerate(top_users, start=1):
        result.append(f"{i}. {user} - {message_count} messages")

    return "\n".join(result)

# Example usage
csv_file = '../csvs/input.csv'  # Replace with your CSV file path
top_10_users = get_top_users_in_channel(csv_file, channel_name='counter-strike', top_n=10)
print(top_10_users)

