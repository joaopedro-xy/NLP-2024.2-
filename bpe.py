import os
import json

def contar_pares_consecutivos(lista):
    # Conta a freq  de pares consecutivos em uma lista.
    frequencia_pares = {}
    
    for i in range(len(lista) - 1):
        par = (lista[i], lista[i + 1])
        
        if par in frequencia_pares:
            frequencia_pares[par] += 1
        else:
            frequencia_pares[par] = 1
    
    return frequencia_pares

def lista_merges(texto_treino, numero_de_substituicoes):
    # faz os  merges de pares consecutivos no texto e retorna as substituições realizadas.
    texto_treino = list(texto_treino.encode("utf-8"))
    substituicoes = {}
    valor_substituto = 256  # Primeiro valor de substituição como no video do karpathy

    for _ in range(numero_de_substituicoes):
        frequencia_pares = contar_pares_consecutivos(texto_treino)
        
        if not frequencia_pares:
            break

        par_mais_frequente = max(frequencia_pares, key=frequencia_pares.get)
        substituicoes[par_mais_frequente] = valor_substituto
        
        i = 0
        while i < len(texto_treino) - 1:
            if (texto_treino[i], texto_treino[i + 1]) == par_mais_frequente:
                texto_treino[i] = valor_substituto
                del texto_treino[i + 1]
            else:
                i += 1

        valor_substituto += 1

    return substituicoes

def merge_all(texto_treino, substituicoes):
    # Aplica todas as substituições ao texto.
    i = 0
    while i < len(texto_treino) - 1:
        par = (texto_treino[i], texto_treino[i + 1])
        
        if par in substituicoes:
            texto_treino[i] = substituicoes[par]
            del texto_treino[i + 1]
            i = 0
        else:
            i += 1

    return texto_treino

def vocabulario(list_all_merges): # aqui decidi ultilizar somente essa a função implementada pelo karpathy para a atividade  
    # Cria um vocabulário a partir de pares combinados.
    vocab = {idx: bytes([idx]) for idx in range(256)}
    for (p0, p1), idx in list_all_merges.items():
        vocab[idx] = vocab[p0] + vocab[p1]
    return vocab 

def encode_string(texto_teste, substituicoes, vocab):
    # Codifica um texto usando substituições e vocabulário.
    texto_teste = list(texto_teste.encode("utf-8"))
    texto_codificado = merge_all(texto_teste, substituicoes)
    return texto_codificado

def decode(ids, vocab): # Decodifica uma lista de IDs em uma string UTF-8.
    tokens = b"".join(vocab[idx] for idx in ids)
    text = tokens.decode("utf-8", errors="replace")
    return text

def decode_ids_to_strings(ids, vocab):
    # Decodifica IDs para suas strings correspondentes usando um vocabulário.
    strings = []
    for id in ids:
        if id in vocab:
            decoded_string = vocab[id].decode("utf-8", errors="replace")
            strings.append(decoded_string)
        else:
            strings.append("")  # Caso não haja mapeamento, adiciona string vazia
    return strings

def concatenar_textos(textos):
    # Concatena uma list de textos em uma única string com delimitador.
    delimitador = "[END]"
    return delimitador.join(texto.strip() for texto in textos) + delimitador

def tokenizer_setup(texto_treino, num_substituicoes):
    # prepara o texto para o tokenizador, gerando substituições e vocabulário.
    if isinstance(texto_treino, list):
        texto_treino = concatenar_textos(texto_treino)
    
    substituicoes = lista_merges(texto_treino, num_substituicoes)
    vocab = vocabulario(substituicoes)
    
    return substituicoes, vocab

def carregar_textos(caminho_pasta):
    # Carrega textos de arquivos JSON em uma lista, extraindo o valor da chave 'text'.
    texto_treino = []
    
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                texto_treino.append(dados['text'])
    
    return texto_treino
