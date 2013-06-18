upvote_by_id = '''UPDATE T_DRINK
        SET upvotes = upvotes + 1
        WHERE drink_id = ?
        '''

downvote_by_id = '''UPDATE drinks
        SET downvotes = downvotes + 1
        WHERE drink_id = ?
        '''