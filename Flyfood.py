def modulo(termOne, termTwo): # Função para determinar o módulo das distâncias
    resultado = termOne - termTwo
    if resultado < 0:
        resultado *= -1
        return resultado
    return resultado


def distancia(termOne, termTwo): # Função para determinar a distância entre dois pontos de entrega
    return termOne+termTwo


def permutar(string): # Função de permutação dos n pontos de entrega para obter todos os possíveis percursos a serem percorridos
    if len(string) == 1:
        return string
    lista = []
    for letra in string:
        string_aux = string.replace(letra, '')
        lista.extend([letra+string for string in permutar(string_aux)])
    return lista


arquivo = open('matriz.txt', 'r')
pontos_entrega = []  # array para armazenar os pontos de entrega
circuitos = []  # array para armazenar todos os possíveis circuitos a serem realizados
coordenadas = {}  # dicionário para armazenar as coordenadas dos pontos de entrega
contador = 0
for linha in arquivo:
    linha = linha.replace(" ","")
    if contador == 0:  # definindo o número de linhas e colunas da matriz
        n = int(linha[0])
        m = int(linha[1])
    elif contador <= n:
        for i in linha:  # verificando linha por linha do arquivo onde estão localizados os pontos de entrega
            if i == 'R':
                coordenadas['R'] = (contador, linha.index(i)+1)
            elif i != '0' and i != '\n':
                pontos_entrega.append(i)
                coordenadas[f'{i}'] = (contador, linha.index(i) + 1)
    contador += 1
# permutando os pontos de entregas para adquirir todos os circuitos possíveis
for i in permutar(''.join(pontos_entrega)):
    circuitos.append(i)
arquivo.close()
contador = 0
tempo = 0 # Variável utilizada para contabilizar o custo em distância do circuito que está sendo testado "chamado de tempo para facilitar o entendimento"
melhorTempo = 0  # Variável utilizada para definir o melhor tempo de todos os circuitos testados. "chamado de melhor tempo para facilitar o entendimento"
melhorCircuito = [[0 for _ in range(1)] for _ in range(1)]
while contador < len(circuitos):
    for i in circuitos[contador]:
        # se é o primeiro ponto de entrega começamos contabilizando a distância do restaurante
        if circuitos[contador].index(i) == 0:
            xOne = coordenadas[f'R'][0]
            xTwo = coordenadas[f'{i}'][0]
            yOne = coordenadas['R'][1]
            yTwo = coordenadas[f'{i}'][1]
            tempo += distancia(modulo(xTwo, xOne), modulo(yTwo, yOne))
            entregaAtual = i

        elif circuitos[contador].index(i) < len(circuitos[contador]) - 1:
            xOne = coordenadas[f'{entregaAtual}'][0]
            xTwo = coordenadas[f'{i}'][0]
            yOne = coordenadas[f'{entregaAtual}'][1]
            yTwo = coordenadas[f'{i}'][1]
            tempo += distancia(modulo(xTwo, xOne ),modulo(yTwo, yOne))
            entregaAtual = i
# Quando chegamos no penultimo ponto, contabilizamos a distância do penúltimo  ponto de entrega até o ultimo e depois do último ponto até o restaurante.
        else:
            xOne = coordenadas[f'{entregaAtual}'][0]
            xTwo = coordenadas[f'{i}'][0]
            yOne = coordenadas[f'{entregaAtual}'][1]
            yTwo = coordenadas[f'{i}'][1]
            tempo += distancia(modulo(xTwo, xOne), modulo(yTwo, yOne))
            xOne = coordenadas[f'{i}'][0]
            xTwo = coordenadas['R'][0]
            yOne = coordenadas[f'{i}'][1]
            yTwo = coordenadas['R'][1]
            tempo += distancia(modulo(xTwo, xOne), modulo(yTwo, yOne))
            # Se esse for o primeiro circuito a ser testado, ele será o melhor circuito e o melhor tempo.
            if contador == 0:
                melhorTempo = tempo
                melhorCircuito[0] = circuitos[contador]
# Se não for o primeiro circuito a ser testado, é verificado se o tempo menor que o melhor tempo encontrado anteriormente
            elif tempo < melhorTempo:
                melhorTempo = tempo
                melhorCircuito[0] = circuitos[contador]
    tempo = 0
    contador += 1
print("O melhor circuito para fazer as entregas é: " + ' '.join(melhorCircuito[0]))
print(melhorTempo)