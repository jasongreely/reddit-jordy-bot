import praw
import re
import db

TARGET_SUB = "crumbumsandbox"

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit(TARGET_SUB)

# Listen to comment stream for Jordy Nelson
for comment in subreddit.stream.comments():
    if re.search("Jordy Nelson", comment.body, re.IGNORECASE):

        print("Jordy comment found {}: {}".format(comment.id, comment.body))

        if db.has_replied(comment.id):
            print("Already replied to comment {}: {}".format(comment.id, comment.body))
        else:
            print("Replying to comment {}: {}".format(comment.id, comment.body))
            db.add_reply(comment.id)
            comment.reply(":(")




