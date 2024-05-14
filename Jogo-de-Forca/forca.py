#forca.py - Jogo da Forca por Rafael Alcântara
import random
from palavras_portugues import PALAVRAS
from string import ascii_uppercase
from sys import exit

def main():
    print("\n***BEM-VINDO AO JOGO DA FORCA! DIVIRTA-SE!!***")
    LETRAS_DO_ALFABETO = set(ascii_uppercase)
    jogo = JogoDaForca(PALAVRAS)
    rodada = 0
    letra_escolhida = ""
    
    while True:
        rodada += 1
        print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")
        print(f"Rodada {rodada})\n")                         
        print(f"Erros cometidos: {jogo.erros}\\7")
        jogo.imprime_forca()
        
        #Usuário escolhe uma letra válida
        while True:
            print("\nEscolha uma letra (a - z): ")
            letra_escolhida = input(">> ").upper()

            if letra_escolhida in jogo.letras_ditas:
                print("\nVocê já falou essa letra.")
            elif letra_escolhida not in LETRAS_DO_ALFABETO:
                print("\nO valor digitado é inválido.")
            else:
                break

        jogo.valida_letra(letra_escolhida)

        if jogo.erros >= 7:
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")
            print(f"Rodada {rodada})\n")                         
            print(f"Erros cometidos: {jogo.erros}\\7")
            jogo.imprime_forca_final()
            print(f"***VOCÊ PERDEU! A PALAVRA ERA '{jogo.palavra}'***")
            break
        elif jogo.letras_palavra.issubset(jogo.letras_ditas) == True:
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")
            print(f"Rodada {rodada})\n")                         
            print(f"Erros cometidos: {jogo.erros}\\7")
            jogo.imprime_forca()
            print("***PARABÉNS, VOCÊ VENCEU!***")
            break
        else:
            continue  

    print("\nVocê gostaria de jogar novamente? (s/n)")
    decisao = input(">> ")

    if decisao.upper() == "S":
        main()
    else:
        exit(0)
        
    
class JogoDaForca(object):
    def __init__(self, lista_de_palavras):
        self.palavra = random.choice(lista_de_palavras).upper()
        self.PARTES_DO_CORPO = ["|","O","-+-","/ | \\","-.-","| |","|_|"] 
        self.cf = ["|","","","","","","___"] #Partes do corpo na forca
        self.letras_palavra = set(self.palavra)
        self.letras_ditas = set()
        self.erros = 0
    
    def monta_corpo(self):
        erros = self.erros 

        for i in range(0, erros):
            self.cf[6-i] = self.PARTES_DO_CORPO[6-i]

        #Teste:
        #print(f"\nPartes construídas: {self.cf}\n")

    
    def imprime_letras_forca(self):
        palavra = self.palavra
        letras_ditas = self.letras_ditas
        tamanho = len(palavra)

        for letra in palavra:
            if letra in letras_ditas:
                print(f"{letra} ", end='')
            else:
                print("_ ", end='')

        #Teste:
        #print(f" Palavra: {palavra}\n")
    
    
    def imprime_forca(self):
        self.monta_corpo()
        p = self.cf

        print("\nLetras já escolhidas: ", end='')
        for letra in self.letras_ditas:
            print(f"{letra}", end=' ')
            
        #Impresão do boneco na forca
        print("\n_________       ")
        print(f"|       {p[0]}   ")
        print(f"|       {p[0]}   ")
        print(f"|       {p[1]}   ")
        print(f"|      {p[2]}    ")
        print(f"|     {p[3]}     ")
        print(f"|      {p[4]}    ")
        print(f"|      {p[5]}    ")
        print(f"|______{p[6]}____")
        print("|                 ")
        print("|                 ")
        print("|                 ")
        print("|                 ")
        print("|                 ")
        print("|                 ")

        self.imprime_letras_forca()
        print("\n")

    def imprime_forca_final(self):
        print("\nLetras já escolhidas: ", end='')
        for letra in self.letras_ditas:
            print(f"{letra}", end=' ')
            
        #Impresão do boneco na forca
        print("\n_________     ")
        print("|       |       ")
        print("|       |       ")
        print("|       |       ")
        print("|       |       ")
        print("|       O       ")
        print("|      -+-      ")
        print("|     | | |     ")
        print("|_____ -+- ____ ")
        print("|      | |      ")
        print("|      | |      ")
        print("|               ")
        print("| -Você morreu- ")
        print("|               ")
        print("|               ")
        
        self.imprime_letras_forca()
        print("\n")

    def valida_letra(self, letra):
        
        if letra in self.letras_palavra:
            self.letras_ditas.add(letra)
        else: 
            self.erros += 1
            self.letras_ditas.add(letra)


main()
    
    



    
    
    

