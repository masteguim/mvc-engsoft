import tkinter as tk
from tkinter import messagebox, ttk


class BookstoreView:
    """View: interface gráfica, sem regras de negócio."""

    def __init__(self, root):
        self.root = root
        self.root.title("Livraria Aurora")
        self.root.geometry("1000x720")
        self.root.minsize(760, 560)
        self.root.configure(bg="#faf8f4")

        self._search_callback = None
        self._add_callback = None
        self._reserve_callback = None

        self._build_layout()

    def _build_layout(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#faf8f4")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure(
            "Title.TLabel",
            background="#f0e8dd",
            foreground="#302923",
            font=("Georgia", 25, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background="#faf8f4",
            foreground="#45443f",
            font=("Arial", 11),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#292923",
            font=("Georgia", 15, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background="#ffffff",
            foreground="#77776f",
            font=("Arial", 10),
        )
        style.configure(
            "Accent.TButton",
            background="#a94332",
            foreground="#ffffff",
            padding=(10, 7),
            font=("Arial", 10, "bold"),
        )

        header = ttk.Frame(self.root, padding=(24, 18))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="AURORA · LIVRARIA",
            foreground="#a94332",
            background="#faf8f4",
            font=("Georgia", 17, "bold"),
        ).pack(side="left")

        ttk.Label(
            header,
            text="Livros para descobrir, em casa ou na loja",
            style="Body.TLabel",
        ).pack(side="right")

        hero = tk.Frame(
            self.root,
            bg="#f0e8dd",
            padx=28,
            pady=24,
        )
        hero.pack(fill="x")

        ttk.Label(
            hero,
            text="Histórias que encontram você.",
            style="Title.TLabel",
        ).pack(anchor="w")

        tk.Label(
            hero,
            text=(
                "Pesquise o catálogo, adicione livros à sacola "
                "ou reserve para retirar na loja."
            ),
            bg="#f0e8dd",
            fg="#5f5d57",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(8, 0))

        controls = ttk.Frame(
            self.root,
            padding=(24, 18, 24, 8),
        )
        controls.pack(fill="x")

        ttk.Label(
            controls,
            text="Buscar livro:",
            style="Body.TLabel",
        ).pack(side="left", padx=(0, 10))

        self.search_entry = ttk.Entry(
            controls,
            font=("Arial", 11),
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.canvas = tk.Canvas(
            self.root,
            bg="#faf8f4",
            highlightthickness=0,
        )

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.cards_frame = ttk.Frame(self.canvas)

        self.cards_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw",
        )

        self.cards_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.bind("<Configure>", self._resize_cards)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 12),
            pady=5,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(24, 0),
            pady=5,
        )

        store = ttk.LabelFrame(
            self.root,
            text="Unidade Centro",
            padding=12,
        )
        store.pack(fill="x", padx=24, pady=(8, 10))

        ttk.Label(
            store,
            text="Rua das Flores, 120 · Seg. a sáb., das 9h às 20h",
            style="Body.TLabel",
        ).pack(anchor="w")

        footer = ttk.Frame(
            self.root,
            padding=(24, 8, 24, 16),
        )
        footer.pack(fill="x")

        self.cart_label = ttk.Label(
            footer,
            text="Sacola: 0 itens",
            style="Body.TLabel",
        )
        self.cart_label.pack(side="left")

        ttk.Label(
            footer,
            text="MVP da Livraria Aurora · MVC",
            style="Body.TLabel",
        ).pack(side="right")

    def set_callbacks(self, search, add_to_cart, reserve):
        """Recebe do Controller as funções acionadas pela interface."""
        self._search_callback = search
        self._add_callback = add_to_cart
        self._reserve_callback = reserve

    def _on_search(self, _event=None):
        if self._search_callback:
            self._search_callback(self.search_entry.get())

    def _resize_cards(self, event):
        self.canvas.itemconfigure(
            self.cards_window,
            width=event.width,
        )

    def show_books(self, books):
        """Exibe os livros recebidos do Controller."""
        for child in self.cards_frame.winfo_children():
            child.destroy()

        if not books:
            ttk.Label(
                self.cards_frame,
                text="Nenhum livro encontrado.",
                style="Body.TLabel",
                padding=20,
            ).grid(row=0, column=0, sticky="w")
            return

        columns = 2 if self.root.winfo_width() > 800 else 1

        for index, book in enumerate(books):
            row, column = divmod(index, columns)

            card = ttk.Frame(
                self.cards_frame,
                style="Card.TFrame",
                padding=16,
                relief="solid",
                borderwidth=1,
            )
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=7,
                pady=7,
            )

            self.cards_frame.columnconfigure(
                column,
                weight=1,
                uniform="book-card",
            )

            ttk.Label(
                card,
                text=book.category.upper(),
                foreground="#a94332",
                background="#ffffff",
                font=("Arial", 9, "bold"),
            ).pack(anchor="w")

            ttk.Label(
                card,
                text=book.title,
                style="CardTitle.TLabel",
                wraplength=350,
            ).pack(anchor="w", pady=(7, 2))

            ttk.Label(
                card,
                text=book.author,
                style="Muted.TLabel",
            ).pack(anchor="w")

            ttk.Label(
                card,
                text=book.description,
                style="Muted.TLabel",
                wraplength=350,
            ).pack(anchor="w", pady=(9, 5))

            price_text = f"R$ {book.price:.2f}".replace(".", ",")

            ttk.Label(
                card,
                text=price_text,
                background="#ffffff",
                font=("Arial", 13, "bold"),
            ).pack(anchor="w")

            if book.store_stock > 0:
                stock_text = f"{book.store_stock} unidade(s) na loja"
            else:
                stock_text = "Indisponível na loja"

            ttk.Label(
                card,
                text=stock_text,
                style="Muted.TLabel",
            ).pack(anchor="w", pady=(3, 9))

            actions = ttk.Frame(
                card,
                style="Card.TFrame",
            )
            actions.pack(anchor="w")

            ttk.Button(
                actions,
                text="Adicionar à sacola",
                style="Accent.TButton",
                command=lambda book_id=book.id: (
                    self._add_callback(book_id)
                ),
            ).pack(side="left", padx=(0, 6))

            reserve_button = ttk.Button(
                actions,
                text="Reservar para retirada",
                command=lambda book_id=book.id: (
                    self._reserve_callback(book_id)
                ),
            )
            reserve_button.pack(side="left")

            if book.store_stock <= 0:
                reserve_button.state(["disabled"])

    def show_cart_summary(self, quantity, total):
        """Atualiza o resumo da sacola exibido no rodapé."""
        formatted_total = f"R$ {total:.2f}".replace(".", ",")
        self.cart_label.configure(
            text=f"Sacola: {quantity} itens · Total: {formatted_total}"
        )

    def show_info(self, message):
        messagebox.showinfo(
            "Livraria Aurora",
            message,
            parent=self.root,
        )

    def show_error(self, message):
        messagebox.showerror(
            "Livraria Aurora",
            message,
            parent=self.root,
        )