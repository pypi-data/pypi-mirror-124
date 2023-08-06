import os
from twitter import Client

# def __lt__(self, other):
#         if not isinstance(other, PollOptions):
#             raise Exception(f"{other} is not from class PollOptions")
#         return self.position < other.position

#     def __gt__(self, other):
#         if not isinstance(other, PollOptions):
#             raise Exception(f"{other} is not from class PollOptions")
#         return self.position > other.position

client=Client(os.environ['bearer_token'])
tweet=client.get_tweet(1450353845293383683)
user=client.get_user_by_username("TheGenocides")

print(tweet.poll.options[0] > tweet.poll.options[1])
# print(tweet.original_payload)