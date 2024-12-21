import csv

def get_top_messages_by_reactions(csv_file, top_n=50):
    # List to store messages along with their reaction count
    messages = []
    
    # Open and read the CSV file
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV
        for row in reader:
            try:
                # Convert reaction_count to an integer
                reaction_count = int(row['reaction_count'])
                
                # Store the message data in the list
                messages.append({
                    'messageId': row['messageId'],
                    'authorName': row['authorName'],
                    'reaction_count': reaction_count,
                    'messageDate': row['messageDate'],
                    'channelName': row['channelName'],
                    'channelId': row['channelId']
                })
            except ValueError:
                # Skip rows with invalid reaction_count
                continue

    # Sort messages by reaction_count in descending order
    messages_sorted = sorted(messages, key=lambda x: x['reaction_count'], reverse=True)
    
    # Get the top N messages
    top_messages = messages_sorted[:top_n]

    # Format and return the top N messages with URLs
    result = []
    for message in top_messages:
        message_url = f"https://discord.com/channels/384396975925231647/{message['channelId']}/{message['messageId']}"
        result.append(
            f"Message ID: {message['messageId']}\n"
            f"Author: {message['authorName']}\n"
            f"Reactions: {message['reaction_count']}\n"
            f"Date: {message['messageDate']}\n"
            f"Channel: {message['channelName']}\n"
            f"URL: {message_url}\n"
        )
    
    return "\n".join(result)

# Example usage
csv_file = '../csvs/input.csv'  # Replace with your CSV file path
top_50_messages = get_top_messages_by_reactions(csv_file, top_n=50)
print(top_50_messages)

