# pylint: disable=R0903
class Reference:

    # pylint: disable=R0913
    # pylint: disable=R0917
    def __init__(self, citekey, author, title, year: int, publisher):
        self.citekey = citekey
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher

    def __str__(self):
        return f"{self.citekey}, {self.author}, {self.title}, {self.year}, {self.publisher}"
