class Book:
    def __init__(self, title, author, isbn, publication_date, copies_available):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_date = publication_date
        self.copies_available = copies_available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_date": self.publication_date,
            "copies_available": self.copies_available
        }