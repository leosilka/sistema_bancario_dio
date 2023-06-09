import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Saque Indisponível! Você não tem saldo suficiente!")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque realizado! Você sacou R${valor:.2f}!")
            return True

        else:
            print("Operação Cancelada! O valor está incorreto!")

        return False

    def depositar(self, valor):
        saldo = self.saldo

        if valor > 0:
            self._saldo += valor
            print(f"Depósito realizado! Você depositou R${valor:.2f}")

        else:
            print("Operação Cancelada! O valor está incorreto!")

    @property
    def historico(self):
        return self._historico

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes
                             if transacao["tipo:"] == Saque.__name__])

        if valor > self.limite:
            print("Operação Cancelada! Valor de saque acima do permitido!")

        elif numero_saques >= self.limite_saque:
            print("Operação Cancelada! Você atingiu o limite de saque diário!")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C: {self.numero}
            Titulo: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo:": transacao.__class__.__name__,
                "valor:": transacao.valor,
                "data:": datetime.now().strftime("%d-%m-%y  %H:%M:%S"),
            }
        )


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)

        if transacao_realizada:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)

        if transacao_realizada:
            conta.historico.adicionar_transacao(self)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return

    valor = float(input("Informe o valor do depósito R$"))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return

    return cliente.contas[0]

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return

    valor = float(input("Informe o valor do saque: R$"))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return

    conta = recuperar_conta(cliente)
    if not conta:
        return

    print("_______________EXTRATO_______________")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não há movimentação encontrada!"
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo:']}: R${transacao['valor:']:.2f}\n"

    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print("_____________________________________")

def criar_conta(clientes, numero_conta, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta Criada!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já cadastrado!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número, bairro, cidade/siga estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Cliente Cadastrado")

def menu():
    menu = """
    ==============================
        SISTEMA BANCARIO v3
    ==============================
        [1] - DEPOSITAR 
        [2] - SACAR
        [3] - EXTRATO
        [4] - NOVA CONTA
        [5] - LISTAR CONTA
        [6] - NOVO USUÁRIO
        [7] - SAIR
    ==============================
    """
    return input(textwrap.dedent(menu))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(clientes, numero_conta, contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "7":
            return print("Obrigado por usar nossos serviços! Ate mais 😊")

        else:
            print("Você digitou uma opção inválida! Selecione uma opção válida!")
            continue

main()