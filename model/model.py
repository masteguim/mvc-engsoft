
from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    id: int
    title: str
    author: str
    category: str
    price: float
    store_stock: int
    description: str


@dataclass(frozen=True)
class Reservation:
    customer_name: str
    book: Book


class BookstoreModel:
    """Model: catálogo e regras de negócio da livraria."""

    def __init__(self):
        self._books = [
            Book(1, "1984", "George Orwell", "Ficção", 39.90, 6,
                 "Um clássico sobre vigilância, poder e liberdade."),
            Book(2, "O Hobbit", "J. R. R. Tolkien", "Fantasia", 49.90, 3,
                 "A aventura de Bilbo Bolseiro pela Terra-média."),
            Book(3, "Dom Casmurro", "Machado de Assis", "Literatura brasileira", 29.90, 0,
                 "O romance clássico de Bentinho e Capitu."),
            Book(4, "O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil", 24.90, 8,
                 "Uma história sobre amizade e o que é essencial."),
            Book(5, "Código Limpo", "Robert C. Martin", "Tecnologia", 89.90, 2,
                 "Práticas para escrever software mais legível."),
        ]
        self._cart = []
        self._reservations = []

    def search_books(self, query=""):
        term = query.strip().casefold()
        if not term:
            return list(self._books)
        return [book for book in self._books if
                term in book.title.casefold()
                or term in book.author.casefold()
                or term in book.category.casefold()]

    def get_book(self, book_id):
        return next((book for book in self._books if book.id == book_id), None)

    def add_to_cart(self, book_id):
        book = self.get_book(book_id)
        if book is None:
            raise ValueError("Livro não encontrado.")
        self._cart.append(book)
        return book

    def get_cart_summary(self):
        return len(self._cart), sum(book.price for book in self._cart)

    def reserve_for_pickup(self, customer_name, book_id):
        name = customer_name.strip()
        if not name:
            raise ValueError("Informe seu nome para fazer a reserva.")
        book = self.get_book(book_id)
        if book is None:
            raise ValueError("Livro não encontrado.")
        if book.store_stock <= 0:
            raise ValueError("Este livro está indisponível na loja.")
        reservation = Reservation(name, book)
        self._reservations.append(reservation)
        return reservation

