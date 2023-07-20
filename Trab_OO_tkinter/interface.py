from tkinter import *
from tkinter import simpledialog, messagebox

class Produto:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco

class Carrinho:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def remover_produto(self, produto):
        self.produtos.remove(produto)

    def calcular_total(self):
        total = sum(produto.preco for produto in self.produtos)
        return round(total, 2)

class OptionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, options):
        self.prompt = prompt
        self.options = options
        super().__init__(parent, title)

    def body(self, master):
        Label(master, text=self.prompt).grid(row=0, column=0, columnspan=2)
        self.choice = StringVar(master)
        self.choice.set(self.options[0])
        for i, option in enumerate(self.options):
            Radiobutton(master, text=option, variable=self.choice, value=option).grid(row=i + 1, column=0, columnspan=2)

    def apply(self):
        self.result = self.choice.get()

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Supermercado Preço Bão")
        self.geometry("600x400")

        self.catalogo = [
            Produto(1, "Arroz", 10.99),
            Produto(2, "Feijão", 7.50),
            Produto(3, "Macarrão", 3.20),
            Produto(4, "Leite", 4.50),
            Produto(5, "Banana", 2.99),
            Produto(6, "Tomate", 3.75),
            Produto(7, "Pão de Forma", 5.25),
            Produto(8, "Café", 8.80),
            Produto(9, "Refrigerante", 6.99),
            Produto(10, "Biscoito", 2.50)
        ]

        self.carrinho = Carrinho()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="Supermercado do Tião", font=("Arial", 16))
        self.label.pack(pady=20)

        self.add_product_btn = Button(self, text="Adicionar Produto", command=self.add_product)
        self.add_product_btn.pack(pady=10)

        self.remove_product_btn = Button(self, text="Remover Produto", command=self.remove_product)
        self.remove_product_btn.pack(pady=10)

        self.checkout_btn = Button(self, text="Finalizar Compra", command=self.checkout)
        self.checkout_btn.pack(pady=10)

        self.quit_btn = Button(self, text="Sair", command=self.quit)
        self.quit_btn.pack(pady=10)

    def add_product(self):
        product_id = simpledialog.askinteger("Adicionar Produto", "Digite o ID do produto:")
        product = next((produto for produto in self.catalogo if produto.codigo == product_id), None)

        if product:
            self.carrinho.adicionar_produto(product)
            messagebox.showinfo("Produto Adicionado", f"{product.nome} adicionado ao carrinho.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado no catálogo.")

    def remove_product(self):
        if self.carrinho.produtos:
            product_id = simpledialog.askinteger("Remover Produto", "Digite o ID do produto a ser removido:")
            product = next((produto for produto in self.carrinho.produtos if produto.codigo == product_id), None)

            if product:
                self.carrinho.remover_produto(product)
                messagebox.showinfo("Produto Removido", f"{product.nome} removido do carrinho.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado no carrinho.")
        else:
            messagebox.showerror("Erro", "O carrinho está vazio.")

    def checkout(self):
        if self.carrinho.produtos:
            total = self.carrinho.calcular_total()

            opcoes_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito"]
            dialog = OptionDialog(self, "Pagamento", "Escolha o método de pagamento:", opcoes_pagamento)
            metodo_pagamento = dialog.result

            if metodo_pagamento:
                if metodo_pagamento == "Dinheiro":
                    quantia_fornecida = simpledialog.askfloat("Pagamento em Dinheiro", f"Total da compra: R$ {total}\nDigite a quantia fornecida:")
                    troco = quantia_fornecida - total
                    messagebox.showinfo("Compra Finalizada", f"Compra finalizada. Troco: R$ {round(troco, 2)}")
                else:
                    messagebox.showinfo("Compra Finalizada", f"Compra finalizada. Total: R$ {total:.2f}")

                self.carrinho.produtos.clear()
            else:
                messagebox.showerror("Erro", "Método de pagamento inválido.")
        else:
            messagebox.showerror("Erro", "O carrinho está vazio. Adicione produtos antes de finalizar a compra.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
