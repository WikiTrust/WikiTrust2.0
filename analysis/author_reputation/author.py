class Author:
    def __init__(self, starting_reputation):
        self.reputation = starting_reputation

    def get_author_rep(self):
        return self.reputation

    def set_author_rep(self, new_author_rep):
        self.reputation = new_author_rep

    @classmethod
    def check_same_author(cls, author_1, author_2):
        pass