class Reference:
    
    def __init__(self, author, title, year: int, publisher):
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher

    def __str__(self):
        return f"{self.author}, {self.title}, {self.year}, {self.publisher}"