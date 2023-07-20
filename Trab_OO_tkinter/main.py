from enum import Enum
from datetime import datetime

class TipoCalculadora(Enum):
    JUROS_SIMPLES = 1
    JUROS_COMPOSTOS = 2

class DescricaoProduto:
    def __init__(self, id, preco, descricao):
        self.id = id
        self.preco = preco
        self.descricao = descricao

class Endereco:
    def __init__(self, logradouro, complemento, numero, cidade, bairro, uf, cep):
        self.logradouro = logradouro
        self.complemento = complemento
        self.numero = numero
        self.cidade = cidade
        self.bairro = bairro
        self.uf = uf
        self.cep = cep

class ItemVenda:
    def __init__(self, descricao_produto, quantidade):
        self.descricao_produto = descricao_produto
        self.quantidade = quantidade

    def get_subtotal(self):
        return self.quantidade * self.descricao_produto.preco

    def __str__(self):
        return f"{self.descricao_produto.descricao}\t\t{self.descricao_produto.preco}\t{self.quantidade}\t{self.get_subtotal()}\n"

class Pagamento:
    def __init__(self, quantia_fornecida):
        self.quantia_fornecida = quantia_fornecida

    def __str__(self):
        return f"Quantia Fornecida: R$ {self.quantia_fornecida}"

class PagamentoCartao(Pagamento):
    def __init__(self, quantia_fornecida, operadora, quantidade_parcelas, tipo_calculadora):
        super().__init__(quantia_fornecida)
        self.operadora = operadora
        self.quantidade_parcelas = quantidade_parcelas
        self.tipo_calculadora = tipo_calculadora

    def simular_parcelas(self, quantia, quantidade_parcelas):
        juros = self.consultar_taxa_juros()
        montante_com_juros = self.tipo_calculadora.calcular_montante_com_juros(quantia, quantidade_parcelas, juros)
        return montante_com_juros / quantidade_parcelas

    def consultar_taxa_juros(self):
        taxa_juros = 0.0
        if self.quantidade_parcelas == 2:
            taxa_juros = 2.5
        elif self.quantidade_parcelas == 3:
            taxa_juros = 5.0
        return taxa_juros

    def __str__(self):
        parcelas = self.simular_parcelas(self.quantia_fornecida, self.quantidade_parcelas)
        return f"Tipo de pagamento...: Cartão de Crédito\n{super().__str__()}\nOperadora................: {self.operadora}\nQuantidade de parcelas....: {self.quantidade_parcelas}\nValor de cada parcela...: {parcelas}\nTipo de calculadora usada na transação................: {self.tipo_calculadora}\n"

class PagamentoCheque(Pagamento):
    def __init__(self, quantia_fornecida, banco):
        super().__init__(quantia_fornecida)
        self.banco = banco

    def __str__(self):
        return f"Tipo de pagamento...: Cheque\nQuantia fornecida....: R$ {self.quantia_fornecida}\nBanco................: {self.banco}"

class PagamentoDinheiro(Pagamento):
    def __init__(self, quantia):
        super().__init__(quantia)

    def __str__(self):
        return f"Tipo de pagamento...: Dinheiro\n{super().__str__()}"

class CalculadoraFinanceira:
    def calcular_montante_com_juros(self, montante_inicial, periodo_meses, juros_ao_mes): 
        pass

class CalculadoraJurosCompostos(CalculadoraFinanceira):
    def calcular_montante_com_juros(self, montante_inicial, periodo_meses, juros_ao_mes):
        novo_montante = montante_inicial * (1 + juros_ao_mes) ** periodo_meses
        return novo_montante

    def __str__(self):
        return "Calculadora de juros compostos"

class CalculadoraJurosSimples(CalculadoraFinanceira):
    def calcular_montante_com_juros(self, montante_inicial, periodo_meses, juros_ao_mes):
        total_juros = montante_inicial * periodo_meses * (juros_ao_mes * 0.01)
        novo_montante = montante_inicial + total_juros
        return novo_montante

    def __str__(self):
        return "Calculadora de juros simples"

class CatalogoProdutos:
    def __init__(self):
        self.descricoes_produtos = []
        self.contador_descricoes_produtos = 0

        d1 = DescricaoProduto("01", 10.99, "Arroz")
        d2 = DescricaoProduto("02", 7.50, "Feijão")
        d3 = DescricaoProduto("03", 3.20, "Macarrão")
        d4 = DescricaoProduto("04", 4.50, "Leite")
        d5 = DescricaoProduto("05", 2.99, "Banana")
        d6 = DescricaoProduto("06", 3.75, "Tomate")                                
        d7 = DescricaoProduto("07", 5.25, "Pão de forma")
        d8 = DescricaoProduto("08", 8.80, "Café")
        d9 = DescricaoProduto("09", 6.99, "Refrigerante")
        d10 = DescricaoProduto("10", 2.50, "Biscoito")

        self.descricoes_produtos.extend([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10])

    def get_descricao_produto(self, id):
        for desc in self.descricoes_produtos:
            if desc.id == id:
                return desc
        raise Exception("Descricao Inexistente para o produto ", id)

class Venda:
    def __init__(self, data):
        self.itens_venda = []
        self.esta_completa = False
        self.data = data
        self.pagamento = None

    def criar_item_venda(self, descricao_produto, quantidade):
        item_venda = ItemVenda(descricao_produto, quantidade)
        self.itens_venda.append(item_venda)

    def fazer_pagamento(self, quantia_fornecida):
        self.pagamento = PagamentoDinheiro(quantia_fornecida)
        return self.calcular_troco()

    def fazer_pagamento_cheque(self, quantia_fornecida, banco):
        self.pagamento = PagamentoCheque(quantia_fornecida, banco)

    def fazer_pagamento_cartao(self, quantia_fornecida, operadora, quantidade_parcelas, tipo_calculadora):
        self.pagamento = PagamentoCartao(quantia_fornecida, operadora, quantidade_parcelas, tipo_calculadora)

    def calcular_troco(self):
        return self.pagamento.quantia_fornecida - self.calcular_total_venda()

    def calcular_total_venda(self):
        total_venda = 0.0
        for item_venda in self.itens_venda:
            total_venda += item_venda.descricao_produto.preco * item_venda.quantidade
        return total_venda

    def __str__(self):
        status = "completa" if self.esta_completa else "incompleta"
        data_temp = self.data.strftime("%d/%m/%Y")
        hora_temp = self.data.strftime("%H:%M:%S")
        cabecalho = f"Data: {data_temp} hora: {hora_temp}\n\t\t\t\tStatus da venda: {status}\n\n Descrição\t\tPreço Unitário(R$)\t\tQuantidade\t\tSubtotal(R$) \n"
        corpo = ""

        for item_venda in self.itens_venda:
            corpo += str(item_venda)

        rodape = f"Total à vista (R$)\t\t\t\t\t\t\t{self.calcular_total_venda()}\n\n{str(self.pagamento)}"
        return cabecalho + corpo + rodape

class Registradora:
    def __init__(self, id):
        self.id = id
        self.vendas = []
        self.catalogo = CatalogoProdutos()

    def criar_nova_venda(self):
        venda = Venda(datetime.now())
        self.vendas.append(venda)

    def entrar_item(self, id, quantidade):
        venda = self.get_venda_corrente()
        descricao_produto = self.catalogo.get_descricao_produto(id)
        venda.criar_item_venda(descricao_produto, quantidade)

    def finalizar_venda(self):
        self.get_venda_corrente().esta_completa = True

    def get_venda_corrente(self):
        if self.vendas:
            return self.vendas[-1]
        else:
            raise Exception("Não há vendas correntes.")

    def get_catalogo(self):
        return self.catalogo

    def __str__(self):
        return f"Registradora ID: {self.id}"

class Loja:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.vendas = []
        self.registradoras = []
        self.endereco = endereco

    def adicionar_venda(self, venda):
        self.vendas.append(venda)

    def adicionar_registradora(self, registradora):
        self.registradoras.append(registradora)

    def get_ultima_venda(self):
        if self.vendas:
            return self.vendas[-1]
        else:
            raise Exception("Não há vendas registradas.")

    def get_registradora(self, id):
        for registradora in self.registradoras:
            if registradora.id == id:
                return registradora
        return None

    def __str__(self):
        return f"Nome: {self.nome}\nEndereço: {self.endereco.logradouro}, {self.endereco.numero}, {self.endereco.complemento}, {self.endereco.bairro}, {self.endereco.cidade}, {self.endereco.uf}, {self.endereco.cep}"

class DescricaoProdutoInexistente(Exception):
    pass

def gerar_recibo(registradora, troco):
    venda = registradora.get_venda_corrente()
    data_temp = venda.data.strftime("%d/%m/%Y")
    hora_temp = venda.data.strftime("%H:%M:%S")
    print("")
    print("--------------------------- Supermercado Preço Bão ---------------------------")
    print(f"                             Registradora: {registradora.id}")
    print("\t\t\t\tCUPOM FISCAL")
    print(f"Data: {data_temp} hora: {hora_temp}")
    print(venda)
    print(f"Troco................: R$ {troco}")

def main():
    endereco = Endereco("Rua X", "", 5, "Alfenas", "Aeroporto", "MG", "37130-000")
    loja = Loja("Supermercado Preço Bão", endereco)

    try:
        registradora1 = Registradora("R01")
        loja.adicionar_registradora(registradora1)
        registradora1.criar_nova_venda()

        catalogo = registradora1.get_catalogo()

        registradora1.entrar_item("01", 3)
        registradora1.entrar_item("02", 2)
        registradora1.entrar_item("03", 1)

        registradora1.finalizar_venda()

        total_venda = registradora1.get_venda_corrente().calcular_total_venda()
        registradora1.get_venda_corrente().fazer_pagamento_cartao(total_venda, "American", 1, CalculadoraJurosSimples())

        gerar_recibo(registradora1, 0.0)

        registradora2 = Registradora("R02")
        loja.adicionar_registradora(registradora2)
        registradora2.criar_nova_venda()

        registradora2.entrar_item("08", 3)
        registradora2.entrar_item("01", 2)
        registradora2.entrar_item("09", 1)

        registradora2.finalizar_venda()

        registradora2.get_venda_corrente().fazer_pagamento(100.00)

        gerar_recibo(registradora2, 100 - registradora2.get_venda_corrente().calcular_total_venda())

        registradora3 = Registradora("R03")
        loja.adicionar_registradora(registradora3)

        registradora3.criar_nova_venda()
        registradora3.entrar_item("06", 3)
        registradora3.entrar_item("07", 2)
        registradora3.entrar_item("02", 1)
        registradora3.finalizar_venda()
        registradora3.get_venda_corrente().fazer_pagamento_cheque(registradora3.get_venda_corrente().calcular_total_venda(), "Banco do Brasil")

        gerar_recibo(registradora3, 0.0)

    except DescricaoProdutoInexistente as e:
        print(e)

if __name__ == "__main__":
    main()
