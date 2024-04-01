from utils.helpers import generate_error

# For Book
OUT_OF_STOCK = generate_error(message="Book is out of stock.", code="book_out_of_stock")

# For Borrow
ALREADY_BORROWED = generate_error(
    message="You have already borrowed this book.",
    code="already_borrowed",
)

# For Reserve
ALREADY_RESERVED = generate_error(
    message="You have already reserved this book.",
    code="already_reserved",
)
