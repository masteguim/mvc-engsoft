from tkinter import simpledialog


class BookstoreController:
    """Coordena as ações entre a View e o Model."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.set_callbacks(
            search=self.search_books,
            add_to_cart=self.add_to_cart,
            reserve=self.reserve_book,
        )

        self.search_books("")
        self.update_cart_summary()

    def search_books(self, query):
        books = self.model.search_books(query)
        self.view.show_books(books)

    def add_to_cart(self, book_id):
        try:
            book = self.model.add_to_cart(book_id)
            self.update_cart_summary()
            self.view.show_info(
                f"{book.title} foi adicionado à sacola."
            )
        except ValueError as error:
            self.view.show_error(str(error))

    def reserve_book(self, book_id):
        customer_name = simpledialog.askstring(
            "Reserva para retirada",
            "Digite seu nome:",
            parent=self.view.root,
        )

        if customer_name is None:
            return

        try:
            reservation = self.model.reserve_for_pickup(
                customer_name,
                book_id,
            )

            self.view.show_info(
                f"Reserva feita para {reservation.customer_name}: "
                f"{reservation.book.title}. "
                "Aguarde a confirmação da livraria."
            )
        except ValueError as error:
            self.view.show_error(str(error))

    def update_cart_summary(self):
        quantity, total = self.model.get_cart_summary()
        self.view.show_cart_summary(quantity, total)