class Author:
    def __init__(self, author_id, starting_reputation):
        self.author_id = author_id
        self.reputation = starting_reputation

    def __str__(self):
        return ("Author ID: " + str(self.author_id) + "    Reputation:" + str(self.reputation))

    def get_author_rep(self):
        return self.reputation

    def set_author_rep(self, new_author_rep):
        self.reputation = new_author_rep

    @classmethod
    def check_same_author(cls, author_1, author_2):
        if author_1.author_id == author_2.author_id:
            return True

        return False