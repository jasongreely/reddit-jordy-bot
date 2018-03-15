import praw
import praw_config
import random
import re
import db

TARGET_SUB = "nfl"

THUMBS = {"https://i.imgur.com/kpgvM9u.jpg", "https://i.imgur.com/CopWQe3.jpg", "https://i.imgur.com/39hgtMd.jpg"}
SADS = {"https://i.imgur.com/XL7vyJB.jpg", "https://i.imgur.com/puoyeru.jpg", "https://i.imgur.com/85YHwdc.jpg"}

def main():
    reddit = praw.Reddit(user_agent = praw_config.user_agent,
                         client_id = praw_config.client_id, client_secret = praw_config.client_secret,
                         username = praw_config.username, password = praw_config.password)

    subreddit = reddit.subreddit(TARGET_SUB)

    for comment in subreddit.stream.comments():
        process_comment(comment)


def process_comment(comment):
    if re.search("Jordy", comment.body, re.IGNORECASE) and comment.is_root:

        print("Jordy comment found {}: {}".format(comment.id, comment.body))

        if db.has_replied(comment.id):
            print("Already replied to comment {}: {}".format(comment.id, comment.body))
        else:
            print("Replying to comment {}: {}".format(comment.id, comment.body))
            db.add_reply(comment.id)
            comment.reply(":(")

    if not comment.is_root and hasattr(comment, 'parent'):
        process_sub_comment(comment)


def process_sub_comment(comment):
    parent = comment.parent()
    replied = False
    if hasattr(parent.author, "name"):
        if re.search("JordyDiedForThis", parent.author.name, re.IGNORECASE) and not db.has_replied(comment.id):
            print("Comment is response to bot")
            if re.search("good bot", comment.body, re.IGNORECASE):
                replied = True
                IMG_SRC = random.choice(tuple(THUMBS))
                comment.reply("[:')]({})".format(IMG_SRC))

            else:
                replied = True
                if re.search("bad bot", comment.body, re.IGNORECASE) or re.search("sad bot", comment.body, re.IGNORECASE):
                    IMG_SRC = random.choice(tuple(SADS))
                    comment.reply("[:'(]({})".format(IMG_SRC))

            if replied:
                db.add_reply(comment.id)


main()
