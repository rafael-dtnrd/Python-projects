# Sistema de Banco - Versão 1.1 (Multiusuário) - Rafael Silva de Alcantara
# O sistema deve permitir cadastrar usuários no sistema e permitir que os usuários relizem depósitos, saques, consultas de extratos e alteração de limite diário
# O valor limite de saques diário poderá ser alterado pelo cliente, mas deve corresponder a no máximo 75% do saldo do cliente.

import sys, subprocess
import random

def main():

    print("\n    SEJA BEM-VINDO AO BANCO DIO!")
    agencia1 = dict()

    while True:
        imprimir_menu()
        selecao = input("    Digite a opção desejada.....: ")

        if selecao.upper() == "C":
            clear_screen()
            nome_cliente = input("\n    Digite o nome do cliente.........: ")
            mensagem = "\n    Digite o valor do saldo inicial..: "
            saldo_inicial = solicitar_valor(mensagem)
            criar_conta(agencia=agencia1, nome_cliente=nome_cliente, saldo_inicial=saldo_inicial)

        elif selecao.upper() == "L":
            clear_screen()
            listar_contas(agencia=agencia1)

        elif selecao.upper() =="E":
            clear_screen()
            conta = input("\n    Digite o número da conta..: ")
            exibir_conta(agencia=agencia1, conta=conta)

        elif selecao.upper() == "I":
            clear_screen()
            conta = input("\n    Digite o número da conta..: ")
            imprimir_extrato_conta(agencia=agencia1, conta=conta)

        elif selecao.upper() == "D":
            codigo_transacao = 1
            conta = input("\n    Digite o número da conta..: ")
            mensagem = "\n    Digite o valor do depósito..: "
            valor_deposito= solicitar_valor(mensagem)
            realizar_trasacao_conta(agencia=agencia1, conta=conta, tipo_transacao=codigo_transacao, valor=valor_deposito)

        elif selecao.upper() == "S":
            codigo_transacao = 2
            conta = input("\n    Digite o número da conta..: ")
            mensagem = "\n    Digite o valor do saque.....: "
            valor_saque = solicitar_valor(mensagem)
            realizar_trasacao_conta(agencia=agencia1, conta=conta, tipo_transacao=codigo_transacao, valor=valor_saque)

        elif selecao.upper() == "A":
            codigo_transacao = 3
            conta = input("\n    Digite o número da conta..: ")
            mensagem = "\n    Digite o valor do novo limite.....: "
            novo_limite = solicitar_valor(mensagem)
            realizar_trasacao_conta(agencia=agencia1, conta=conta, tipo_transacao=codigo_transacao, valor=novo_limite)

        elif selecao.upper() == "F":
            break

        else:
            print("\n")
            print(" * Opção inválida! *".center(38, " "))


def clear_screen():

    operating_system = sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell=True)
    elif operating_system == 'linux':
        subprocess.run('clear', shell=True)
    else:
        return None


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
    clear_screen()
    print(menu_inicial)


def solicitar_valor(mensagem):

    while True:
        print(f"{mensagem}", end='')
        entrada = input()

        try:
            entrada = int(entrada)
        except ValueError:
            print("\n   ", end="")
            print("* O valor digitado é inválido! *".center(38, " "))
            continue
        except:
            print("\n   ", end="")
            print("* Algo deu errado! *".center(38, " "))
            break
        else:
            break

    return entrada


def criar_conta(*, agencia, nome_cliente, saldo_inicial):

    nome_cliente = nome_cliente.upper()

    while True:
        numero_conta = random.randint(1000, 9999)

        if str(numero_conta) in agencia.keys():
            continue
        else:
            cliente = Cliente(numero_conta, nome_cliente, saldo_inicial)
            agencia[str(numero_conta)] = cliente
            break

    print("\n   ", end="")
    print(f"* Conta de {nome_cliente.upper()} criada! *".center(38, " "))


def listar_contas(*, agencia):
    if len(agencia.keys()) > 0:
        contas = agencia.keys()
        print("\n   ", end="")
        print(" CONTAS CADASTRADAS".center(50, "="))
        print("\n    Conta   Cliente \n")
        for conta in contas:
            cliente = agencia[conta]
            print(f"    {conta:^5}   {cliente.nome_cliente:<}")
        print("\n   ", end="")
        print(" fim de lista ".center(50, "="))
    else:
        print("\n   ", end="")
        print(" CONTAS CADASTRADAS ".center(50, "="))
        print("")
        print("* Não há clientes cadastrados *".center(50, " "))
        print("\n   ", end="")
        print(" fim de lista ".center(50, "="))

def exibir_conta(*, agencia, conta):
    contas = agencia.keys()

    if conta in contas:
        cliente = agencia[conta]
        cliente.exibir_informacoes()
    else:
        print("\n   ", end="")
        print(f"* Conta inválida! *".center(38, " "))


def imprimir_extrato_conta(*, agencia, conta):
    contas = agencia.keys()

    if conta in contas:
        cliente = agencia[conta]
        cliente.imprimir_extrato()
    else:
        print("\n   ", end="")
        print(f"* Conta inválida! *".center(38, " "))

def realizar_trasacao_conta(*, agencia, conta, tipo_transacao, valor):
    contas = agencia.keys()

    if conta in contas:
        cliente = agencia[conta]

        if tipo_transacao == 1:
            # Realiza depósito
            cliente.depositar(valor)
        elif tipo_transacao == 2:
            # Realiza saque
            cliente.sacar(valor)
        elif tipo_transacao == 3:
            # Altera limite
            cliente.alterar_limite(valor)
        else:
            print("\n   ", end="")
            print("* Algo deu errado! *".center(38, " "))
    else:
        print("\n   ", end="")
        print(f"* Conta inválida! *".center(38, " "))


class Cliente(object):

    def __init__(self, numero_conta, nome_cliente, saldo):
        self.numero_conta = numero_conta
        self.nome_cliente = nome_cliente
        self.saldo = saldo
        self.limite = self.saldo * 0.25
        self.transacoes = list()
        self.numero_saques = 0
        self.valor_saques = 0


    def exibir_informacoes(self):
        print("\n   ", end="")
        print(f" CONTA {self.numero_conta} ".center(50, "="))
        print("")
        print(f"        NOME.......: {self.nome_cliente}")
        print(f"        SALDO......: {self.saldo:.2f}")
        print(f"        LIMITE.....: {self.limite:.2f}")
        print("\n   ", end="")
        print(" fim de informações ".center(50, "="))

    def depositar(self, valor_deposito):
        # Caso o valor do depósito seja maior que zero, o valor do depósito é adicionado ao saldo do usuário
        if valor_deposito > 0:
            saldo_inicial = self.saldo
            self.saldo += valor_deposito
            # Após somar o valor do depósito ao saldo do usuário, um dicionário contendo o tipo de transação, o saldo inicial, o valor do depósito e saldo final é adicionado à lista de transações realizadas
            self.transacoes.append(
                {"tipo_transacao": "C", "saldo_inicial": saldo_inicial, "valor_transacao": valor_deposito,
                 "saldo_final": self.saldo})
            print("\n   ", end="")
            print(f"* Depósito de R$ {valor_deposito:.2f} realizado! *".center(38, " "))
        else:
            print("\n   ", end="")
            print(f"* '{valor_deposito}' não é um valor válido * ".center(38, " "))


    def sacar(self, valor_saque):
        if (valor_saque <= 0):
            print("\n   ", end="")
            print(f"* '{valor_saque}' não é um valor válido *".center(38, " "))
        elif (self.numero_saques > 3):
            print("\n   ", end="")
            print("* Transação negada! *".center(38, " "))
            print("\n    Limite diário de saques atingido.")
        elif (valor_saque > self.saldo):
            print("\n   ", end="")
            print("* Transação negada! *".center(38, " "))
            print("\n    Saldo insuficiente.")
        else:
            if (valor_saque + self.valor_saques > self.limite):
                print("\n   ", end="")
                print("* Valor de saque indisponível! *".center(39, " "))
                print("\n    Observe o limite de saques.")
            else:
                saldo_inicial = self.saldo
                self.saldo -= valor_saque
                self.numero_saques += 1
                self.valor_saques += valor_saque
                # Após realizar o saque, um dicionário contendo o tipo de transação, o saldo inicial, o valor do saque e saldo final é adicionado à lista de transações realizadas
                self.transacoes.append(
                    {"tipo_transacao": "D", "saldo_inicial": saldo_inicial, "valor_transacao": valor_saque,
                     "saldo_final": self.saldo})
                print("\n   ", end="")
                print(f"* Saque de R$ {valor_saque:.2f} realizado! *".center(38, " "))

    def alterar_limite(self, novo_limite):
        if (novo_limite <= 0):
            print("\n   ", end="")
            print(f"* '{novo_limite}' não é um valor válido *".center(38, " "))
        elif (novo_limite > self.saldo * 0.75):
            print("\n   ", end="")
            print("* Transação negada! *".center(38, " "))
            print("\n    O limite não pode superar 75% do seu saldo.")
        else:
            self.limite = novo_limite
            print("\n   ", end="")
            print(f"* Limite alterado para {novo_limite}! *".center(38, " "))


    def imprimir_extrato(self):
        numero_transacoes = len(self.transacoes)

        clear_screen()
        print("\n   ", end="")
        print(" EXTRATO DO DIA ".center(38, "="))

        if numero_transacoes > 0:
            print(f"\n    SALDO INICIAL: R$ {self.transacoes[0]["saldo_inicial"]:.2f}")
            print(f"\n        Transações: {numero_transacoes}\n")
            for transacao in self.transacoes:
                print(f"          {transacao["tipo_transacao"]}  RS {transacao["valor_transacao"]:.2f}")
            print(f"\n    SALDO FINAL: R$ {self.transacoes[numero_transacoes - 1]["saldo_final"]:.2f}\n")
        else:
            print(f"\n    SALDO INICIAL: R$ {self.saldo:.2f}")
            print(f"\n        Transações: {numero_transacoes}")
            print("\n          Nenhuma transação a exibir.")
            print(f"\n    SALDO FINAL: R$ {self.saldo:.2f}\n")
        print("    ", end="")
        print(" fim de extrato ".center(38, "="))


main()

