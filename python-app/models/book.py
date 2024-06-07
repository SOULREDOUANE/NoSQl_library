class Book:
    def __init__(self, title, author, isbn, publication_date, copies_available, cover_url):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_date = publication_date
        self.copies_available = copies_available
        self.cover_url = cover_url

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_date": self.publication_date,
            "copies_available": self.copies_available,
            "cover_url" : self.cover_url
        }