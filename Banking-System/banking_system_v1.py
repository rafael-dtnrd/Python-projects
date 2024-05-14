# Sistema de Banco Uniusuário - Versão 1.0 - Rafael Silva de Alcantara
# O sistema permite a um único usuário relizar depósitos, saques e consultas de extratos.
# O valor máximo de saques diário é de R$500,00

import sys, subprocess

def clear_screen():
    input("\n    Pressione 'ENTER' para OPÇÕES")
    operating_system = sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell=True)
    elif operating_system == 'linux':
        subprocess.run('clear', shell=True)
    else:
        return 0


def main():

    menu_inicial = """
    ========= SISTEMA BANCO DIO =========
    
    OPÇÕES:
    
        E - Imprimir Extrato
        D - Realizar Depósito
        S - Realizar Saque
        F - Finalizar Sistema
        
    =====================================
    """
    usuario = Usuario(2000)
    print("\n    SEJA BEM-VINDO AO BANCO DIO!")

    while True:
        clear_screen()
        print(menu_inicial)
        selecao = input("    Digite a opção desejada.....: ")

        if selecao.upper() == "E":
            usuario.imprimir_extrato()
        elif selecao.upper() == "D":
            while True:
                entrada = input("\n    Digite o valor do depósito..: ")
                try:
                    valor_deposito = int(entrada)
                except ValueError:
                    print("\n   ", end="")
                    print("* O valor digitado é inválido! *".center(38, " "))
                    continue
                except:
                    print("\n   ", end="")
                    print("* Algo deu errado! *".center(38, " "))
                    break
                else:
                    usuario.depositar(valor_deposito)
                    break
        elif selecao.upper() == "S":
            while True:
                entrada = input("\n    Digite o valor do saque.....: ")
                try:
                    valor_saque = int(entrada)
                except ValueError:
                    print("\n   ", end="")
                    print("* O valor digitado é inválido! *".center(38, " "))
                    continue
                except:
                    print("\n   ", end="")
                    print("* Algo deu errado! *".center(38, " "))
                    break
                else:
                    usuario.sacar(valor_saque)
                    break
        elif selecao.upper() == "F":
            print("\n   ", end="")
            print("* Programa finalizado. *".center(38, " "))
            break
        else:
            print("\n   ", end="")
            print("* Opção inválida! *".center(38, " "))


class Usuario(object):

    def __init__(self, saldo=0):
        self.saldo = saldo
        self.transacoes = list()
        self.numero_saques = 0
        self.valor_saques = 0


    def depositar(self, valor_deposito):
        # Caso o valor do depósito seja maior que zero, o valor do depósito é adicionado ao saldo do usuário
        if valor_deposito > 0:
            saldo_inicial = self.saldo
            self.saldo += valor_deposito
            # Após somar o valor do depósito ao saldo do usuário, um dicionário contendo o tipo de transação, o saldo inicial, o valor do depósito e saldo final é adicionado à lista de transações realizadas
            self.transacoes.append({"tipo_transacao": "C", "saldo_inicial": saldo_inicial, "valor_transacao": valor_deposito, "saldo_final": self.saldo})
            print("\n   ", end="")
            print(f"* Depósito de R$ {valor_deposito:.2f} realizado! *".center(38, " "))
        else:
            print("\n   ", end="")
            print(f"* '{valor_deposito}' não é um valor válido.* ".center(38, " "))
    def sacar(self, valor_saque):
        if (valor_saque <= 0):
            print("\n   ", end="")
            print(f"* '{valor_saque}' não é um valor válido. *".center(38, " "))
        elif (self.numero_saques > 3):
            print("\n   ", end="")
            print("* Transação negada! *".center(38, " "))
            print("\n    Limite diário de saques atingido.")
        elif (valor_saque > self.saldo):
            print("\n   ", end="")
            print("* Transação negada. *".center(38, " "))
            print("\n    Saldo insuficiente.")
        else:
            if (valor_saque + self.valor_saques > 500):
                print("\n   ", end="")
                print("* Valor de saque indisponível! *".center(39, " "))
                print("\n    Observe o limite de saques.")
            else:
                saldo_inicial = self.saldo
                self.saldo -= valor_saque
                self.numero_saques += 1
                self.valor_saques += valor_saque
                # Após realizar o saque, um dicionário contendo o tipo de transação, o saldo inicial, o valor do saque e saldo final é adicionado à lista de transações realizadas
                self.transacoes.append({"tipo_transacao": "D", "saldo_inicial": saldo_inicial, "valor_transacao": valor_saque, "saldo_final": self.saldo})
                print("\n   ", end="")
                print(f"* Saque de R$ {valor_saque:.2f} realizado! *".center(38, " "))

    def imprimir_extrato(self):
        numero_transacoes = len(self.transacoes)

        operating_system = sys.platform

        if operating_system == 'win32':
            subprocess.run('cls', shell=True)
        elif operating_system == 'linux':
            subprocess.run('clear', shell=True)
        else:
            return 0

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

