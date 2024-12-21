import csv
from collections import defaultdict

def parse_csv_and_calculate_reactions(file_path):
    # Dictionary to hold the total reactions and names for each authorId
    reactions_by_author = defaultdict(lambda: {'total_reactions': 0, 'author_name': ''})

    # Open and read the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV
        for row in reader:
            author_id = row['authorId']
            reaction_count = int(row['reaction_count'])
            author_name = row['authorName']

            # Aggregate the reaction count for the given authorId and store the authorName
            reactions_by_author[author_id]['total_reactions'] += reaction_count
            reactions_by_author[author_id]['author_name'] = author_name

    # Return the results as a sorted list of tuples:
    # - First, by total_reactions in descending order
    # - Second, by author_id in ascending order
    return sorted(
        [(author_id, data['author_name'], data['total_reactions']) for author_id, data in reactions_by_author.items()],
        key=lambda x: (-x[2], x[0])  # Sort by total_reactions descending, then by author_id ascending
    )

# Usage example
file_path = '../csvs/input.csv'  # Replace with your CSV file path
author_reactions = parse_csv_and_calculate_reactions(file_path)

# Print the results
for author_id, author_name, total_reactions in author_reactions:
    print(f'Author ID: {author_id}, Author Name: {author_name}, Total Reactions: {total_reactions}')

