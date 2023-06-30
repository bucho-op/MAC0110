import sys
import analisadorléxico


def main():
    arquivos = sys.argv[1:]
    for arquivo in arquivos:
        arquivo = arquivo[:-2]
        arqComment = analisadorléxico.commentcheck(arquivo) # a variável arComment guarda uma string com o texto após a remoção de comentários
        arqPosComment = open(arquivo + "temp.txt", "w") # este open dá write no arquivo temporário
        arqPosComment.write(arqComment) # ~~~~
        arqPosComment.close()
        lista, linha = analisadorléxico.tokenização(arquivo) # aqui é chamada a função de token, tendo como argumento o arquivo do terminal
        listaPosGen = analisadorléxico.generalização(lista)
        analisadorléxico.gravação(listaPosGen, arquivo, linha)

main()

