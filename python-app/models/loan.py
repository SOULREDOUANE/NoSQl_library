class Loan:
    def __init__(self, book_id, borrower_name, loan_date, return_date, status):
        self.book_id = book_id
        self.borrower_name = borrower_name
        self.loan_date = loan_date
        self.return_date = return_date
        self.status = status