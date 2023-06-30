from écomentáriooustring import écomentáriooustring

def commentcheck(arquivo):
    arq = open(arquivo + "py", "r") # abre o arquivo para a leitura
    line = True
    temp = "" # inicializa variável que vai guardar o texto do arquivo
    arquivo_atualizado = "" # inicializa variável que vai guardar o texto do arquivo
    while line: # laço para leitura linha a linha
        i = 0
        line = arq.readline()    
        comentario = True
        while comentario and i < len(line): # este laço é responsável por remover os comentários do tipo '#'
            if line[i] == "#" and écomentáriooustring(line, i) == True:
                comentario = False
                temp += '\n'
            else:
                temp += line[i]
            i += 1


    arq = open(arquivo +"temp.txt", "x")
    arq.close()
    arq = open(arquivo +"temp.txt", "w")
    arq.write(temp)
    arq.close()
    arq = open(arquivo +"temp.txt", "r")

    line = True
    comentario = True
    while line:
        k = 0
        line = arq.readline()
        while k < len(line):
            if line[k:k+3] == '"""':
                comentario = not comentario
                k = k + 2         
            elif comentario:
                arquivo_atualizado += line[k]
            k += 1
    
    return arquivo_atualizado


def letterchecking(line, id, i):
    e_id = False # variável booleana que dirá se o elemento pertence ou não ao alfabeto
    while i < len(line) and e_id == False: # varre a string
        k = 0
        stop = True
        while k < len(id) and stop == True: # varre os elementos do alfabeto
            if i == len(line) - 1 and line[i] == id[k]: # se ele for o último da linha e for identificador
                i += 1 # soma mais um pra entrar no intervalo quando fizer o slice [inicio:fim] para pegar o id inteiro        
                stop = False
            elif line[i] == id[k]: # testa se line[i] é um elemento do alfabeto e não é último de linha
                i += 1 # soma 1 na iteração de i
                e_id = True
            k += 1
        if e_id == True: # se o elemento pertence ao alfabeto ou não é o último da linha
            e_id = False # o laço deve continuar
        else:
            e_id = True # senão ele deve parar (essa condição if/else, poderia ser subsituída por 'e_alfabeto = not e_alfabeto')
    fim = i
    return fim
    
def endentcheck(linha, oldendent, arquivo, linha1, lineCount):
    linha = str(linha)
    lenlinha = len(linha) # calcula o len dessa string
    linha = linha.lstrip()
    newlenlinha = len(linha) #clacula o len da string sem a identação
    endent = lenlinha - newlenlinha # registra essa diferença na variável endent
    saveEndent = endent # salva o valor da endentação
    if endent < oldendent: # este if para os casos em que a identação atual é menor, vai adicionar 'END' dependendo da diferença de identação
        arquivo.append("END")
        linha1.append(lineCount + 1) # + 1 pois a endentação é feita na linha seguinte
    elif endent > oldendent: # este fará exatamente a mesma coisa só que para o caso que endent > oldendent
        arquivo.append("BEGIN")
        linha1.append(lineCount + 1)
    return saveEndent, arquivo, linha1 # retorna a nova endentação, para que em seguida, ela vire a antiga, ao ser atribuída na def tokenização



def tokenização(arq):
    arqOpen = open(arq + "temp.txt", "r") # recebe o sysargv aqui, e acrescenta o sufixo temp, chamando aquele arquivo temporário salvo na main
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÃÕÊÂabcdefghijklmnopqrstuvwxyzáéíóúãõêâ_"
    id = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÃÕÊÂabcdefghijklmnopqrstuvwxyzáéíóúãõêâ_0123456789"

    arquivo = [] # cria a lista em que vai guardar o arquivo
    oldendent = 0 # inicializa um primeiro valor padrão para a endentação
    line = True # usado no laço de while que percorre as linhas do arquivo
    lineCount = 0
    linha = [] # usada para criar o arquivo .lin da gravação
    while line:
        line = arqOpen.readline()
        oldendent, arquivo, linha = endentcheck(line, oldendent, arquivo, linha, lineCount) # função que aplica a endentação na linha se necessário
        i = 0 # i deve ser reinicializado a cada iteração de linha
        lineCount += 1 # contador das linhas
        while i < len(line):
            m = 0
            ta_na_lista = False
            while m < len(alfabeto) and not ta_na_lista:
                if line[i] == alfabeto[m]:
                    ta_na_lista = True
                else:
                    m += 1
            # este laço while acima checa se o elemento pode ser o início de uma id e guarda isso na variável booleana ta_na_lista 
            if line[i].isspace() == True:
                line[i].isspace() == True # checa primeiro se o caracter lido é um espaço e, se for, apenas pula para o próximo
            elif ta_na_lista:
                for k in range(len(alfabeto)): # varre o alfabeto (que contém também _)
                    if i < len(line) and line[i] == alfabeto[k]:
                        inicio = i # encontra o índice de início do identificador
                        fim = letterchecking(line, id, i) # função que encontra os elementos do identificador
                        i = fim # atualiza o i para o ponto atual de varredura da string line
                        if fim <= len(line):  # Check if fim is within the bounds of line
                            arquivo.append(line[inicio:fim])
                        else:
                            arquivo.append(line[inicio:fim + 1])  # Append the remaining characters of line
                    # caso line[i] não pertença ao alfabeto o laço while apenas segue em frente
                i = i - 1 # isso aqui é feito para que a próxima iteração while seja encontre o índice correto a ser computado
            
            elif line[i].isdigit(): # teste se o elemento lido é um dígito
                inicio = i # guarda o índice inicial
                notdigit = True # cria a variável notdigit para demarcar o momento em que line[i] não é um dígito (i.e, o fim do laço)
                i += 1 # contagem
                while i < len(line) and notdigit == True: # cria o laço
                    if line[i].isdigit() == True:
                        i += 1 # se for verdade, conta mais um
                    else: # senão, ocorre a saída do laço
                        notdigit = False
                fim = i # guarda o primeiro índice após o final do número
                arquivo.append(line[inicio:fim])
                i = i - 1 # aqui a lógica usada é a mesma no caso anterior
            else:
                arquivo.append(line[i]) # cobre o terceiro caso
            if line[i].isspace() == False: # isso aqui será usado na fase de gravação, para facilitar o trabalho
                linha.append(lineCount)
            i += 1 # contador de cada caractere da linha
    arqOpen.close() # fecha o manuseio do arquivo
    return arquivo, linha # retorna o arquivo fatiado registrado em uma string

def generalização(lista): # a função de generalizar identificadores vai iterar em cada elemento do arquivo
# terá o objetivo de trocar para "var" (se for um id genérico) e "fun" (se for um id do python).
    reserved = [ 'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'form', 'global', 'if',
'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÃÕÊÂabcdefghijklmnopqrstuvwxyzáéíóúãõêâ_"
    for k in range(len(lista)):
        elem = str(lista[k])  
        reservedId = True # variável irá identificar se o elemento é uma palavra reservada
        for i in range(len(reserved)): # reserved é uma lista que contém todos as palavras reservadas
            if elem == reserved[i]:
                reservedId = False # demarca o fato de que é uma palavra reservada
        anyId = True # variável irá identificar se é um id genérico
        for j in range(len(alfabeto)): # irá checar se o primeiro caractere está na string alfabeto(i.e., se é um id)
            if elem[0] == alfabeto[j] and elem != "BEGIN" and elem != "END":
                anyId = False
        
        
        if reservedId == False: # se for uma palavra reservada
            lista[k] = 'fun'
        elif anyId == False: # se for um id genérico
            lista[k] = 'var'
    return lista

def gravação(lista, arquivo, linha):
    arq = open(arquivo + "len", "x")
    arq.close()
    arq = open(arquivo + "len", 'w')
    arq.write(str(lista))
    arq.close()
    # salva o .len pedido no enunciado
 

    arq = open(arquivo + "lin", "x")
    arq.close()
    arq = open(arquivo + "lin", 'w')
    arq.write(str(linha))
    arq.close()
