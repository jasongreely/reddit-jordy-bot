import mysql_config

cnx = mysql_config.cnx


def get_all():
    """
    Retrieve the full data set from the `comments` table
    :return:
    """

    cursor = cnx.cursor(buffered=True,dictionary=True)

    query = "SELECT `id`, `commentid`, `dateAdded` FROM `comments`"

    cursor.execute(query)

    for (id, comment_id, dateAdded) in cursor:
        print("index {}, comment ID {}, date {}".format(id, comment_id, dateAdded))

    cursor.close()


def add_reply(comment_id):
    """
    Insert a comment reference into the `comments` table
    :param comment_id:
    :return:
    """

    cursor = cnx.cursor()

    insert = "INSERT INTO comments (commentid) VALUES ('{}')".format(comment_id)

    cursor.execute(insert)

    print("Comment {} added as row: {}".format(comment_id, cursor.lastrowid))
    cnx.commit()
    cursor.close()


def has_replied(comment_id):
    """
    Checks `comment` database for an existing comment to ensure duplicate responses do not occur
    :param comment_id:
    :return reply_found:
    """

    reply_found = False
    cursor = cnx.cursor()

    query = "SELECT `id`, `commentid` FROM `comments` WHERE `commentid` = '{}'".format(comment_id)
    print("Has replied query: {}".format(query))

    cursor.execute(query)

    for (id, reply_comment_id) in cursor:
        if comment_id == reply_comment_id:
            print("Comment found, #{}: {}".format(id, reply_comment_id))
            reply_found = True

    return reply_found


def close():
    mysql_config.close()