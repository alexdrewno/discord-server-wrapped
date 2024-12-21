from datetime import datetime, timezone
import discord

class DiscordClient(discord.Client):
    async def on_ready(self):
        """
            Implementing discord.Client on_ready() that is called when the bot is ready

            We do any additional post-initialization set-up here
        """
        print('Logged on as {0}!'.format(self.user))
    
    async def on_message(self, message):
        """
            Implementing discord.Client on_message() that is called when a user messages
            in a server (discord.Guild)

            This is where all of the commands are called for the DiscordClient
        """
        if message.author == self.user:
            return

        if len(message.content) < 1:
            return

        if message.content != '/do secret thing hehe':
            return


        await self.get_all_messages(message.guild)

    async def get_all_messages(self, guild):
        print("Started to get all messages.")
        text_channel_list = []
        parsed_messages = []
        last_message = None

        # Set the start and end dates for the year 2024
        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        
        for channel in guild.text_channels:
            text_channel_list.append(channel)
            print(f"Started to get all messages for {channel.name}.")

            # Get messages from the channel
            # discord.py handles rate limiting internally
            messages = []
            async for message in channel.history(limit=100):
                if start_date > message.created_at or end_date < message.created_at:
                    continue
                parsed_message = parse_message(message, channel)
                parsed_messages.append(parsed_message)
                messages.append(message)


            # Now, let's paginate (get more messages before the last one)
            last_message = messages[-1] if messages else None

            while last_message:
                print(f"fetched {len(parsed_messages)}")

                # Get the next batch of messages before the last fetched message
                fetched_messages = channel.history(limit=100, before=last_message)
                messages = []
                async for message in fetched_messages:
                    if start_date > message.created_at or end_date < message.created_at:
                        continue
                    parsed_message = parse_message(message, channel)
                    parsed_messages.append(parsed_message)
                    messages.append(message)

                # Update last_message to be the new most recent message in the current batch
                if (len(messages) > 0):
                    last_message = messages[-1]
                else: 
                    last_message = None
        

        print(f"Parsed {len(parsed_messages)} messages.")

        with open('discord_messages.csv', 'w') as file:
            file.write(csv_header_row())
            for m in parsed_messages:
                file.write(parsed_message_to_csv_row(m))

        print("Wrote results to csv file")

def parse_message(message, channel):
    messageObj = {}
    messageObj['messageId'] = message.id
    messageObj['authorId'] = message.author.id
    messageObj['authorName'] = message.author.name
    messageObj['authorGlobalName'] = message.author.global_name
    messageObj['bot'] = message.author.bot 
    messageObj['reactionsCount'] = get_reaction_count(message) 
    messageObj['messageDate'] = message.created_at
    messageObj['channelId'] = channel.id
    messageObj['channelName'] = channel.name
    return messageObj

def csv_header_row():
    csv_row = ""
    csv_row += 'messageId,'
    csv_row += 'authorId,'
    csv_row += 'authorName,'
    csv_row += 'authorGlobalName,'
    csv_row += 'bot,'
    csv_row += 'reaction_count,'
    csv_row += 'messageDate,'
    csv_row += 'channelId,'
    csv_row += 'channelName'
    csv_row += '\n'
    return csv_row


def parsed_message_to_csv_row(parsed_message):
    csv_row = ""
    csv_row += str(parsed_message['messageId']) + ','
    csv_row += str(parsed_message['authorId']) + ','
    csv_row += str(parsed_message['authorName']) + ','
    csv_row += str(parsed_message['authorGlobalName']) + ','
    csv_row += str(parsed_message['bot']) + ','
    csv_row += str(parsed_message['reactionsCount']) + ','
    print(parsed_message['reactionsCount'])
    csv_row += str(parsed_message['messageDate']) + ','
    csv_row += str(parsed_message['channelId']) + ','
    csv_row += str(parsed_message['channelName'])
    csv_row += '\n'
    return csv_row

def get_reaction_count(message):
    count = 0
    for react in message.reactions:
        count += react.count
    return count

