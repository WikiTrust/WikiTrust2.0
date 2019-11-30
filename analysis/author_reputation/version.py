class Version:
    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __str__(self):
        return "Version " + str(self.author.author_id) +"\n Text: " + self.text
