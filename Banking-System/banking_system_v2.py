# Sistema de Banco - Versão 2.0 (Multiusuário) - Rafael Silva de Alcantara
from datetime import datetime
from abc import ABC, abstractmethod
from random import randint
import sys, subprocess


def main() -> None:
    print("\n    SEJA BEM-VINDO AO BANCO DIO!")
    Sistema.imprimir_menu()


class ID:
    def __init__(self, prefixo: str = "") -> None:
        self._prefixo = prefixo
        self._lista_id = []


    def __str__(self) -> str:
        ids: str = ""
        if len(self._lista_id) == 0:
            ids = "Empty list"
        elif len(self._lista_id) == 1:
            ids = "[" + str(self._lista_id[0]) + "]"
        else:
            for i, id in enumerate(self._lista_id):
                if i == 0:
                    ids += "[" + str(id) + ", "
                elif i == len(self._lista_id) - 1:
                    ids += str(id) + "]"
                else:
                    ids += str(id) + ", "
        return ids


    def gerar_id(self) -> str:
        numero_id: int = randint(1, 1_000_000)
        prefixo: str = self._prefixo + (7 - len(str(numero_id))) * "0"
        _id: str = prefixo + str(numero_id)
        while _id in self._lista_id:
            numero_id: int = randint(1, 1_000_000)
            _id: str = self._prefixo + str(numero_id)
        self._lista_id.append(_id)
        return _id


class Transacao(ABC):
    @property
    @abstractmethod
    def id_transacao(self):
        pass


    @property
    @abstractmethod
    def tipo_transacao(self):
        pass


    @property
    @abstractmethod
    def valor(self):
        pass


    @property
    @abstractmethod
    def timestamp(self):
        pass


    def __str__(self) -> str:
        return f"[id_transacao: {self.id_transacao}, tipo-valor: {self.tipo_transacao} - {self.valor}, timestamp: {self.timestamp}]"


class Deposito(Transacao):
    def __init__(self, valor: float, id_transacao: ID) -> None:
        self._id_transacao = id_transacao.gerar_id()
        self._tipo_transacao = 'C'
        self._valor = valor
        self._timestamp = datetime.now()


    @property
    def id_transacao(self) -> str:
        return self._id_transacao


    @property
    def tipo_transacao(self) -> str:
        return self._tipo_transacao


    @property
    def valor(self) -> float:
        return self._valor


    @property
    def timestamp(self) -> datetime:
        return self._timestamp


class Saque(Transacao):
    def __init__(self, valor: float, id_transacao: ID) -> None:
        self._id_transacao = id_transacao.gerar_id()
        self._tipo_transacao = 'D'
        self._valor = valor
        self._timestamp = datetime.now()


    @property
    def id_transacao(self) -> str:
        return self._id_transacao


    @property
    def tipo_transacao(self) -> str:
        return self._tipo_transacao


    @property
    def valor(self) -> float:
        return self._valor


    @property
    def timestamp(self) -> datetime:
        return self._timestamp


class Historico:
    def __init__(self):
        self._transacoes = {}


    def __str__(self) -> str:
        output: str = ""
        for i, transacao in enumerate(self._transacoes.values()):
            if i == 0:
                output += f"[{i}: {transacao}, \n"
            elif i == len(self._transacoes.values()) - 1:
                output += f"{i}: {transacao}]"
            else:
                output += f"{i}: {transacao}, \n"
        return output


    @property
    def transacoes(self) -> dict:
        return self._transacoes


    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes[transacao.id_transacao] = transacao


class Conta:
    def __init__(self, id_agencia: str, id_cliente: str, id_conta: ID) -> None:
        self._id_agencia = id_agencia
        self._id_cliente = id_cliente
        self._id_conta = id_conta.gerar_id()


    @property
    def id_agencia(self) -> str:
        return self._id_agencia or None


    @property
    def id_cliente(self) -> str:
        return self._id_cliente or None


    @property
    def id_conta(self) -> str:
        return self._id_conta or None


class ContaCorrente(Conta):
    def __init__(self, id_agencia: str, id_cliente: str, id_conta: ID, *, saldo: float) -> None:
        super().__init__(id_agencia, id_cliente, id_conta)
        self._saldo = saldo
        self._limite = 500.00
        self._limite_saques = 3
        self._historico = Historico()


    @property
    def saldo(self) -> float:
        return self._saldo


    @property
    def limite(self) -> float:
        return self._limite


    @property
    def limite_saques(self) -> int:
        return self._limite_saques


    @property
    def historico(self) -> Historico:
        return self._historico


    def __str__(self) -> str:
        return \
        f"""
        CONTA {self.id_conta} 
        
            SALDO..............: {self.saldo:.2f}
            LIMITE.............: {self.limite:.2f}            
            LIMITE DE SAQUES...: {self.limite_saques}
        """


    def set_saldo(self, novo_saldo: float) -> None:
        if novo_saldo >= 0:
            self._saldo = novo_saldo
        else:
            raise ValueError("Limite da conta deve ser maior que zero.")


    def set_limite(self, novo_limite) -> None:
        if novo_limite >= 0 and novo_limite <= self.saldo:
            self._limite = novo_limite
            print(f"        * Limite alterado para {novo_limite:.2f}! *")
        else:
            raise ValueError("Valor de limite inválido.")


    def set_limite_saques(self, novo_limite) -> None:
        if novo_limite >= 0:
            self._limite_saques = novo_limite
            print(f"        * Limite de saques alterado para {novo_limite}! *")
        else:
            raise ValueError("Valor de limite de saques inválido.")


    def registrar_transacao(self, transacao: Transacao) -> None:
        """
        Adiciona uma transação ao histórico de transações da conta

        :param transacao: Transacao
        :return: None
        """
        self._historico.adicionar_transacao(transacao)



    def depositar(self, valor_deposito: float, id_transacao: ID) -> None:
        """
        Soma um valor do depósito ao saldo da conta caso o valor de depósito seja válido.

        :param valor_deposito: float
        :param id_transacao: ID
        :return: Transacao
        """

        if valor_deposito < 0:
            print(f"        * '{valor_deposito:.2f}' não é um valor válido * ")
        else:
            novo_saldo: float = self.saldo + valor_deposito
            try:
                self.set_saldo(novo_saldo)
            except ValueError:
                print(f"        * '{valor_deposito:.2f}' não é um valor válido * ")
            else:
                deposito: Transacao = Deposito(valor_deposito, id_transacao)
                self.registrar_transacao(deposito)
                print(f"        * Depósito de R$ {valor_deposito:.2f} realizado na conta {self.id_conta}! *")


    def sacar(self, valor_saque: float, id_transacao: ID) -> None:
        """
        Conta o número de saques realizados no dia da chamada da função e diminui o valor de saque do saldo
        caso o valor seja válido e o número de saques e o limite de saques não tenham sido ultrapassados.

        :param valor_saque: float
        :param id_transacao: ID
        :return: Transacao
        """

        if valor_saque < 0:
            print(f"        * '{valor_saque:.2f}' não é um valor válido * ")
        else:
            data_transacao = datetime.now().date()
            saques_dia: dict = {'valor_saques': 0, 'numero_saques': 0}

            if len(self.historico.transacoes.values()) != 0:
                for transacao in self.historico.transacoes.values():
                    if transacao.timestamp.date() == data_transacao:
                        saques_dia['valor_saques'] += transacao.valor
                        saques_dia['numero_saques'] += 1
                    else:
                        continue

            if saques_dia['numero_saques'] > self.limite_saques or saques_dia['valor_saques'] > self.limite:
                raise ValueError("O Limite diário de número ou valor de saques já foi atingido.")
            elif valor_saque + saques_dia['valor_saques'] > self.limite:
                raise ValueError("Verifique o limite diário de saques.")
            else:
                novo_saldo: float = self.saldo - valor_saque
                try:
                    self.set_saldo(novo_saldo)
                except ValueError as erro:
                    print(f"        * {erro} *")
                else:
                    saque: Transacao = Saque(valor_saque, id_transacao)
                    self.registrar_transacao(saque)
                    print(f"        * Saque de R$ {valor_saque:.2f} realizado na conta {self.id_conta}! *")

    def imprimir_historico(self) -> str:
        """
        Imprime informações da conta e conjunto de transações da mesma

        :return: str
        """
        output: str = "        TRANSAÇÕES\n\n"
        if len(self.historico.transacoes.values()) == 0:
            output += "            * Não houve transações nesta conta. *\n"
        else:
            for transacao in self.historico.transacoes.values():
                output += f"            {transacao.timestamp.strftime("%d-%m-%Y")}: {transacao.tipo_transacao} - {transacao.valor}\n"
        return output


class Cliente:
    def __init__(self, id_agencia: str, id_cliente: ID) -> None:
        self._id_agencia = id_agencia
        self._id_cliente = id_cliente.gerar_id()
        self._contas = {}


    @property
    def id_agencia(self) -> str:
        return self._id_agencia


    @property
    def id_cliente(self) -> str:
        return self._id_cliente


    @property
    def contas(self) -> dict:
        return self._contas


    def adicionar_conta_corrente(self, id_conta: ID, saldo: float) -> ContaCorrente:
        """
        Cria nova conta-corrente e a adiciona ao dicionário de contas do cliente

        :param id_conta: ID
        :param saldo: float
        :return: None
        """
        nova_conta_corrente: ContaCorrente = ContaCorrente(self._id_agencia, self._id_cliente, id_conta, saldo=saldo)
        self._contas[nova_conta_corrente.id_conta] = nova_conta_corrente
        return nova_conta_corrente

    def validar_conta_corrente(self, id_conta: str) -> ContaCorrente:
        """
        Valida a existência de um conta a partir de seu id.

        :param id_conta: str
        :return: ContaCorrente
        """
        if id_conta in self._contas.keys():
            return self._contas[id_conta]
        else:
            raise ValueError("Valor de 'id_conta' inválido.")


    def realizar_transacao(self, *, id_conta: str, valor: float, tipo_transacao: str, id_transacao: ID) -> None:
        """
        Realiza um saque ou deposito em uma conta e cria um objeto do tipo transação do mesmo.

        :param id_conta: str
        :param valor: float
        :param tipo_transacao: str ( 'deposito' | 'saque' )
        :param id_transacao: ID
        :return: None
        """
        conta: ContaCorrente = self.validar_conta_corrente(id_conta)

        if tipo_transacao == 'deposito':
            try:
                conta.depositar(valor, id_transacao)
            except ValueError as erro:
                print(f"        * {erro} *")
        elif tipo_transacao == 'saque':
            try:
                conta.sacar(valor, id_transacao)
            except ValueError as erro:
                print(f"        * {erro} *")
        else:
            raise ValueError("Tipo de transação inválida.")


    def alterar_limite_conta(self, *, id_conta: str, novo_limite:float) -> None:
        """
        Altera o valor do limite de uma conta.

        :param id_conta: str
        :param novo_limite: float
        :return: None
        """
        try:
            conta: ContaCorrente = self.validar_conta_corrente(id_conta)
        except ValueError as erro:
            print(f"        * {erro} *")
        else:
            try:
                conta.set_limite(novo_limite)
            except ValueError as erro:
                print(f"        * {erro} *")


    def imprimir_extrato_conta(self, id_conta: str) -> None:
        """
        Imprime as informações e conjunto de transações de yma conta do cliente

        :param id_conta: str
        :return: str
        """
        try:
            conta: ContaCorrente = self.validar_conta_corrente(id_conta)
        except ValueError as erro:
            print(f"        * {erro} *")
        else:
            print(f"\n        Cliente: {self.id_cliente} - Agência: {self.id_agencia}")
            print(conta)
            print(conta.imprimir_historico())


class PessoaFisica(Cliente):
    def __init__(self, id_agencia: str, id_cliente: ID, nome: str, sobrenome: str, cpf: str, data_nascimento: str, endereco: str = "") -> None:
        super().__init__(id_agencia, id_cliente)
        self._nome = nome
        self._sobrenome = sobrenome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._endereco = endereco


    @property
    def nome_completo(self) -> str:
        return self._nome + self._sobrenome


    @property
    def data_nascimento(self) -> datetime:
        return datetime.strptime(self._data_nascimento, '%d-%m-%Y')


    @property
    def idade(self):
        return datetime.now() - self.data_nascimento


    def __str__(self) -> str:
        return \
        f"""
            Nome..............: {self._nome}
            Sobrenome.........: {self._sobrenome}
            Cpf...............: {self._cpf}
            Data de Nascimento: {self._data_nascimento}
            Endereço..........: {self._endereco}
        """


class Agencia:
    banco = "DIO"

    def __init__(self, id_agencia: ID) -> None:
        self._id_agencia = id_agencia.gerar_id()
        self._clientes = {}


    @property
    def id_agencia(self) -> str:
        return self._id_agencia or None


    @property
    def numero_clientes(self) -> int:
        return len(self._clientes.keys())


    def __str__(self) -> str:
        return f"       Banco {self.banco} - Agência {self.id_agencia} - Número de Clientes: {self.numero_clientes}"


    def adicionar_cliente_pf(self, cliente_pf: PessoaFisica) -> str:
        self._clientes[cliente_pf.id_cliente] = cliente_pf
        return "        * Novo cliente cadastrado! *"


    def pesquisar_cliente(self, id_cliente: str) -> Cliente:
        if id_cliente in self._clientes.keys():
            return self._clientes[id_cliente]
        else:
            raise ValueError("Valor de 'id_conta' inválido.")


    def listar_clientes(self) -> None:
        print("        LISTA DE CLIENTES", end="\n\n")
        for cliente in self._clientes.values():
            print(f"            {cliente.id_cliente}")
        print("")


class Sistema:
    @staticmethod
    def clear_screen():
        operating_system = sys.platform

        if operating_system == 'win32':
            subprocess.run('cls', shell=True)
        elif operating_system == 'linux':
            subprocess.run('clear', shell=True)
        else:
            return None


    @staticmethod
    def imprimir_menu():
        menu_inicial = """
        ========= SISTEMA BANCO DIO =========

            OPÇÕES:

                C - Criar Conta
                L - Listar Contas
                E - Exibir Conta
                I - Imprimir Extrato 
                D - Realizar Depósito 
                S - Realizar Saque
                A - Alterar Limite
                F - Finalizar Sistema

        =====================================
        
        """

        input("\n    Pressione 'ENTER' para OPÇÕES")
        Sistema.clear_screen()
        print(menu_inicial)




if __name__ == '__main__':
    main()
