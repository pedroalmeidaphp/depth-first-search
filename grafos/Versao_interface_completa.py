import PySimpleGUI as sg

def load_lista(file_name):
    vertices = []
    adjacency_list = {}
    # Código de carregamento do arquivo
    with open(file_name, 'r') as file:
        lines = file.readlines()
        num_vertices = int(lines[0].strip().split()[0])
        vertices = list(range(1, num_vertices + 1))
        
        for line in lines[1:]:
            origin, destiny = map(int, line.strip().split())
            N = num_vertices
            adjacency_list.setdefault(origin, []).append(destiny)
            adjacency_list.setdefault(destiny, [])

    for v in adjacency_list:
        adjacency_list[v].sort()
    vertices.sort()
    print(adjacency_list)
    return adjacency_list, N

def imprime(d, f, N):
    output = ''
    for i in range(N):
        output += f'\nVertice {i + 1}: Cinza = {d[i]}; Preto = {f[i]}\n '
    return output

def imprimeVet(d,f):
    return f'\n\nVetor D:{d} \nVetor F:{f}\n\n'

def DFS_visit(b):
    global mark, lista_adj, cor, d, f, output_text
    cor[b] = "Cinza"
    mark = mark + 1
    d[b-1] = mark

    if b in lista_adj:
        for v in lista_adj[b]:
            if cor[v] == "Branco":
                output_text += f"Aresta ({b}, {v}): Árvore\n"
                DFS_visit(v)
            elif cor[v] == "Cinza":
                output_text += f"Aresta ({b}, {v}): Retorno\n"
            elif d[b-1] < f[v-1]:
                output_text += f"Aresta ({b}, {v}): Avanço\n"
            else:
                output_text += f"Aresta ({b}, {v}): Cruzamento\n"

    cor[b] = "Preto"
    mark = mark + 1
    f[b-1] = mark

def DFS():
    global cor, d, f, mark, lista_adj, N, output_text
    
    for u in V:
        cor[u-1] = "Branco"
    cor = ['Branco'] * (N + 1)

    # Descobrindo os "graus" de cada vetor
    grau_saida = [(u, len(lista_adj[u])) for u in V]
    # Compara o segundo elemento pra ordenar os Vertices de maior grau
    grau_saida.sort(key=lambda x: x[1], reverse=True)
    V_ordenado = [v[0] for v in grau_saida]

    output_text = ''
    
    for u in V_ordenado:
        if cor[u] == "Branco":
            DFS_visit(u)
    
    output_text += imprime(d, f, N)
    output_text += imprimeVet(d, f)
    print('\n')
    

layout = [
    [sg.Text('Escolha um arquivo de grafo:')],
    [sg.Input(key='arquivo_grafo'), sg.FileBrowse()],
    [sg.Button('Executar DFS'), sg.Button('Sair')],
    [sg.Multiline(size=(50, 10), key='resultado', disabled=True)],
]

janela = sg.Window('Algoritmo DFS com PySimpleGUI', layout)

# Loop principal
while True:
    event, values = janela.read()
    
    if event in (sg.WINDOW_CLOSED, 'Sair'):
        break
    
    elif event == 'Executar DFS':
        file_name = values['arquivo_grafo']
        print(file_name)
        if file_name.lower().endswith('.txt'):
            [lista_adj, N] = load_lista(file_name)
            V = list(range(1, N + 1))
            cor = ['Branco'] * N
            d = [0] * N
            f = [0] * N
            mark = 0
            DFS()
            output = imprime(d, f, N)
            janela['resultado'].update(output_text)
        else:
            sg.popup_error('Por favor, escolha um arquivo com extensão .txt.')   

janela.close()