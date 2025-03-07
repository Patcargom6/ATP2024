# FUNÇÕES PRINCIPAIS DO SISTEMA
import json

# Carregar Base de Dados Para a Memória -> FUNÇÃO DE ARRANQUE
def Carregar_BD(fnome):

    with open(fnome, 'r', encoding='utf-8') as f:
        publicações = json.load(f)
    return publicações

mybd = Carregar_BD('ata_medica_papers.json')

# Criar Publicação (OPERAÇÃO CRUD)
def Criar_Pub(bd, title, keywords, abstract, publish_date, doi, pdf, url, authors):
    
    nova_pub = {

    'abstract': abstract,
    'keywords': keywords,
    'authors': authors,
    'doi': doi,
    'pdf': pdf,
    'publish_date': publish_date,
    'title': title,
    'url': url

    }

    nova_pub = {campo: entrada for campo, entrada in nova_pub.items() if entrada}
    # Converter dicionário numa lista de tuplos 
    #   -> Se tuplo não tiver uma entrada válida é removido da lista 
    #       -> Atualizar o dicionário sem os campos vazios

    if nova_pub.get('title'): 
        bd.append(nova_pub)
        with open('ata_medica_papers.json', 'w', encoding='utf-8') as f:
            json.dump(bd, f, ensure_ascii=False, indent=4)
    else:
        print(f'A publicação não apresenta um título válido.')

# Apagar Publicação (OPERAÇÃO CRUD)
def Apagar_Pub(bd, title):

    try: 
        remover_pubs = [publicação for publicação in bd if publicação.get('title','').strip(' .').lower() == title.strip(' .').lower()]
        bd_atualizada = [publicação for publicação in bd if publicação.get('title','').strip(' .').lower() != title.strip(' .').lower()]

        if remover_pubs:
            try:

                with open('pub_removidas.json', 'r', encoding='utf-8') as f:
                    pub_removidas = json.load(f)

            except FileNotFoundError:
                    pub_removidas = [] # Inicializamos o ficheiro como uma lista vazia caso não exista
        
            pub_removidas.extend(remover_pubs) # O método .extend() irá adicionar cada publicação removida da bd principal à lista de apagados
            # Utilizamos o método .extend() em vez do método .append(), uma vez que o extend irá adicionar cada elemento de um iterável à lista de apagados em vez de adicionar o iterável em si
            
            with open('pubs_removidas.json', 'w', encoding='utf-8') as f:
                json.dump(pub_removidas, f, ensure_ascii=False, indent=4) # Adicionamos a lista de apagados ao seu ficheiro distinto
                
        with open('ata_medica_papers.json', 'w', encoding='utf-8') as f:
            json.dump(bd_atualizada, f, ensure_ascii=False, indent=4)
        
        print(f'Publicações removidas: {remover_pubs}')
        return remover_pubs
    
    except json.JSONDecodeError: # Se existir alguma formatação incorreta 
        print("Erro: O ficheiro contém dados inválidos.")

# Recuperar Publicações Apagadas
def Recuperar_Pub(fnome):

    with open(fnome, 'r', encoding='utf-8') as f: # Lemos o ficheiro das publicações apagadas
        pub_apagadas = json.load(f)

    with open('ata_medica_papers.json', 'r', encoding='utf-8') as f2: # Lemos o ficheiro principal com a nossa bd
        bd = json.load(f2)

    for publicação in pub_apagadas:
        bd.append(publicação)

    with open('ata_medica_papers.json', 'w', encoding='utf-8') as f2: #Abrimos o ficheiro principal para escrita e implementamos a nova bd atualizada com as publicações recuperadas
        json.dump(bd, f2, ensure_ascii=False, indent=4)

    with open(fnome, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4) # Apagamos as publicações que foram recuperadas do ficheiro de apagados

# Consultar Publicação pelo Título (OPERAÇÃO CRUD)
def Consultar_Title(bd, busca_title):

    for publicação in bd:
        if publicação.get('title') and publicação['title'].lower().strip(' .') == busca_title.lower().strip(' .'):
            print("=== Detalhes da Publicação ===\n")
            print(f"Título: {publicação['title']}")
            if publicação.get('abstract'):
                print(f"Resumo: {publicação['abstract']}")
            if publicação.get('keywords'):
                print(f"Palavras-chave: {publicação['keywords']}")
            if publicação.get('doi'):
                print(f"DOI: {publicação['doi']}")
            if publicação.get('pdf'):
                print(f"PDF: {publicação['pdf']}")
            if publicação.get('publish_date'):
                print(f"Data de Publicação: {publicação['publish_date']}")
            if publicação.get('url'):
                print(f"URL: {publicação['url']}")

            # Não utilizamos blocos elif neste caso, uma vez que interferem com a lógica das condições
            #   -> Ao utilizar blocos elif depois do primeiro if as condições definidas nos blocos elif não seriam demonstradas nos detalhes da publicação

            print("\n--- Autores ---")

            for autor in publicação['authors']:
                print(f"Nome: {autor.get('name', 'Nome não disponível')} ::: "
                          f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                          f"ORCID: {autor.get('orcid', 'ORCID não disponível')}")
            return publicação
        
    return (f'Nenhuma publicação encontrada com o título "{busca_title}".')

# Consultar Publicação pelo PDF (OPERAÇÃO CRUD)
def Consultar_PDF(bd, busca_PDF):
    
    for publicação in bd:
        if publicação.get('pdf') and publicação['pdf'].lower() == busca_PDF.lower().strip():
            print("=== Detalhes da Publicação ===\n")
            print(f"Título: {publicação['title']}")
            if publicação.get('abstract'):
                print(f"Resumo: {publicação['abstract']}")
            if publicação.get('keywords'):
                print(f"Palavras-chave: {publicação['keywords']}")
            if publicação.get('doi'):
                print(f"DOI: {publicação['doi']}")
            if publicação.get('pdf'):
                print(f"PDF: {publicação['pdf']}")
            if publicação.get('publish_date'):
                print(f"Data de Publicação: {publicação['publish_date']}")
            if publicação.get('url'):
                print(f"URL: {publicação['url']}")

            # Não utilizamos blocos elif neste caso, uma vez que interferem com a lógica das condições
            #   -> Ao utilizar blocos elif depois do primeiro if as condições definidas nos blocos elif não seriam demonstradas nos detalhes da publicação

            print("\n--- Autores ---")

            for autor in publicação['authors']:
                print(f"Nome: {autor.get('name', 'Nome não disponível')} ::: "
                          f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                          f"ORCID: {autor.get('orcid', 'ORCID não disponível')}")
            return publicação
        
    return (f'Nenhuma publicação encontrada com o PDF: {busca_PDF}.')

# Consultar Publicação pelo DOI (OPERAÇÃO CRUD)
def Consultar_DOI(bd, busca_DOI):

    for publicação in bd:
        if publicação.get('doi') and publicação['doi'].lower() == busca_DOI.lower().strip():
            print("=== Detalhes da Publicação ===\n")
            print(f"Título: {publicação['title']}")
            if publicação.get('abstract'):
                print(f"Resumo: {publicação['abstract']}")
            if publicação.get('keywords'):
                print(f"Palavras-chave: {publicação['keywords']}")
            if publicação.get('doi'):
                print(f"DOI: {publicação['doi']}")
            if publicação.get('pdf'):
                print(f"PDF: {publicação['pdf']}")
            if publicação.get('publish_date'):
                print(f"Data de Publicação: {publicação['publish_date']}")
            if publicação.get('url'):
                print(f"URL: {publicação['url']}")

            # Não utilizamos blocos elif neste caso, uma vez que interferem com a lógica das condições
            #   -> Ao utilizar blocos elif depois do primeiro if as condições definidas nos blocos elif não seriam demonstradas nos detalhes da publicação

            print("\n--- Autores ---")

            for autor in publicação['authors']:
                print(f"Nome: {autor.get('name', 'Nome não disponível')} ::: "
                          f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                          f"ORCID: {autor.get('orcid', 'ORCID não disponível')}")
            return publicação
        
    return (f'Nenhuma publicação encontrada com o DOI: {busca_DOI}.')

# Consultar Publicação pelo URL (OPERAÇÃO CRUD)
def Consultar_URL(bd, busca_URL):

    for publicação in bd:
        if publicação.get('url') and publicação['url'].lower() == busca_URL.lower().strip():
            print("=== Detalhes da Publicação ===\n")
            print(f"Título: {publicação['title']}")
            if publicação.get('abstract'):
                print(f"Resumo: {publicação['abstract']}")
            if publicação.get('keywords'):
                print(f"Palavras-chave: {publicação['keywords']}")
            if publicação.get('doi'):
                print(f"DOI: {publicação['doi']}")
            if publicação.get('pdf'):
                print(f"PDF: {publicação['pdf']}")
            if publicação.get('publish_date'):
                print(f"Data de Publicação: {publicação['publish_date']}")
            if publicação.get('url'):
                print(f"URL: {publicação['url']}")

            # Não utilizamos blocos elif neste caso, uma vez que interferem com a lógica das condições
            #   -> Ao utilizar blocos elif depois do primeiro if as condições definidas nos blocos elif não seriam demonstradas nos detalhes da publicação

            print("\n--- Autores ---")

            for autor in publicação['authors']:
                print(f"Nome: {autor.get('name', 'Nome não disponível')} ::: "
                          f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                          f"ORCID: {autor.get('orcid', 'ORCID não disponível')}")
            return publicação
        
    return (f'Nenhuma publicação encontrada com o URL: {busca_URL}.')

# Atualizar uma Publicação (OPERAÇÃO CRUD)
def Atualizar_Pub(bd, busca_title, alterar_chave, update_chave, nome_autor, update_autor): 

    pub_encontrada = False

    for publicação in bd:
        if publicação.get('title') and busca_title.strip(' .').lower() == publicação['title'].lower().strip(' .'):
            
            pub_encontrada = True
            print("=== Detalhes da Publicação ===\n")
            print(f"title: {publicação['title']}")
            if publicação.get('abstract'):
                print(f"abstract: {publicação['abstract']}")
            if publicação.get('keywords'):
                print(f"keywords: {publicação['keywords']}")
            if publicação.get('doi'):
                print(f"doi: {publicação['doi']}")
            if publicação.get('pdf'):
                print(f"pdf: {publicação['pdf']}")
            if publicação.get('publish_date'):
                print(f"publish_date: {publicação['publish_date']}")
            if publicação.get('url'):
                print(f"url: {publicação['url']}")

            # Não utilizamos blocos elif neste caso, uma vez que interferem com a lógica das condições
            #   -> Ao utilizar blocos elif depois do primeiro if as condições definidas nos blocos elif não seriam demonstradas nos detalhes da publicação

            print("\n--- Autores ---")

            for autor in publicação['authors']:
                print(f"name: {autor.get('name', 'Nome não disponível')} ::: "
                          f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                          f"orcid: {autor.get('orcid', 'ORCID não disponível')}")
        
            if alterar_chave.strip().lower() and update_chave:
                    publicação[alterar_chave] = update_chave.strip()
            
            elif nome_autor and update_autor:
                for author in publicação.get('authors'):
                    if author.get('name').strip().lower() == nome_autor.strip().lower():
                        if alterar_chave in author:
                                author[alterar_chave] = update_autor.strip()
            
    if pub_encontrada:
        with open('ata_medica_papers.json', 'w', encoding='utf-8') as f:
            json.dump(bd, f, ensure_ascii=False, indent=4)
        print('Publicação alterada com sucesso!')
        return publicação
    print(f"Nenhuma publicação encontrada com o título '{busca_title}'.")
    return None

# Listar Autores na Base de Dados
def Listar_Autores(bd):

    autor_pub = {} # Dicionário onde vamos armazenar as publicações de cada autor -> Chave: nome do autor, Valor: lista de publicações

    for publicação in bd:
        for author in publicação.get('authors'):
            if author['name'] not in autor_pub:
                autor_pub[author['name']] = []
            if publicação.get('title'):
                autor_pub[author['name']].append(publicação['title']) # Para cada autor adicionamos à lista o título de todas as suas publicações

    print('---- Lista de Autores ----')
    for autor, pub in autor_pub.items(): # O método .items() cria uma lista de tuplos que temos de desmembrar
        print(f'\nAutor: {autor}\nPublicações:')
        for title in pub:
            print(f' * {title}')

    return autor_pub

# Listar Publicações de X Autor na Base de Dados
def Listar_Pub_Autor(bd, busca_author):
    
    pub_encontrada = False
    resultado = []

    resultado.append("\n---- Publicações do Autor ----\n")
    for publicação in bd:
        for author in publicação.get('authors'):
            if busca_author.lower().strip() == author['name'].lower():    
                resultado.append(f'* Publicação: {publicação.get('title')}\n')
                pub_encontrada = True
    
    if not pub_encontrada:
        print(f'Nenhuma publicação encontrada para o autor: {busca_author}.')
    return resultado

# Listar Publicações de X Afiliação na Base de Dados
def Listar_Pub_Afil(bd, busca_afil):
    
    pub_encontrada = False
    pub_dupla = [] # Utilizamos uma lista para nos certificarmos que não aparece a mesma publicação duas vezes quando existem dois autores com a mesma afiliação numa publicação 
    resultado = []

    resultado.append("---- Publicações da Afiliação ----\n")
    for publicação in bd:
        for author in publicação.get('authors'):
            if author.get('affiliation') and busca_afil.lower().strip(' .') == author['affiliation'].lower().strip(' .'):
                if publicação['title'] not in pub_dupla:
                    pub_dupla.append(publicação['title'])
                    resultado.append(f'* Publicação: {publicação['title']}\n')
                    pub_encontrada = True
    
    if not pub_encontrada:
        print(f'Nenhuma publicação encontrada para a afiliação: {busca_afil}.')
    return resultado

# Listar Publicações Com X Palavras-Chave na Base de Dados
def Listar_Pub_PC(bd, palavra_chave):
    
    resultado = []

    resultado.append('---- Lista de Publicações ----\n')
    for publicação in bd:
        if publicação.get('keywords'):
            if palavra_chave.lower().strip(' .') in publicação.get('keywords').lower().strip(' .'):
                resultado.append(f'* Publicação: {publicação.get('title')}\n')
    print(f'Nenhuma publicação foi encontrada para a palavra-chave: {palavra_chave}.')
    return resultado

# Listar Publicações Com X Data de Publicação na Base de Dados
def Listar_Data_Pub(bd, data_pub):

    resultado = []

    resultado.append('---- Lista de Publicações ----\n')
    for publicação in bd:
        if publicação.get('publish_date') and data_pub.strip() == publicação.get('publish_date'):
            resultado.append(f'* Publicação: {publicação['title']}\n')
    print(f'Nenhuma publicação foi encontrada para a data: {data_pub}.')
    return resultado

# Importar Registos de Ficheiros Externos Para a Base de Dados
def Importar_Pub(fnome):

    try:
        with open(fnome, 'r', encoding='utf-8') as f: # Lemos o ficheiro externo
            novos_registos = json.load(f)

        with open('ata_medica_papers.json', 'r', encoding='utf-8') as f2: # Lemos o ficheiro principal com a nossa bd
            bd = json.load(f2)

        title_existe = {pub.get('title') for pub in bd if pub.get('title')} # sets em compreensão garante que não haverá duplicados
        pdf_existe = {pub.get('pdf') for pub in bd if pub.get('pdf')}
        doi_existe = {pub.get('doi') for pub in bd if pub.get('doi')}
        url_existe = {pub.get('url') for pub in bd if pub.get('url')}

        mensagens_duplicadas = []

        for registos in novos_registos:
            if registos.get('title') and (registos.get('title') in title_existe or
                registos.get('pdf') in pdf_existe or
                registos.get('doi') in doi_existe or
                registos.get('url') in url_existe
            ): # Os registos válidos no ficheiro externo serão adicionados à bd
                mensagens_duplicadas.append(f'Publicação duplicada "{registos.get('title')}" não foi importada!')     
            else:
                bd.append(registos)

        with open('ata_medica_papers.json', 'w', encoding='utf-8') as f2: #Abrimos o ficheiro principal para escrita e implementamos a nova bd atualizada com os novos registos
            json.dump(bd, f2, ensure_ascii=False, indent=4)

        return mensagens_duplicadas
    
    except json.JSONDecodeError: # Se existir alguma formatação incorreta 
        print("Erro: O ficheiro contém dados inválidos.")

# DISTRIBUIÇÕES DAS PUBLICAÇÕES NA BASE DE DADOS

# Distribuição TOP 20 Autores com Mais Publicações
def Distribuição_20A(bd):

    res = {}
    for publicação in bd:
        for author in publicação['authors']:
            nome_autor = author.get('name')
            if nome_autor in res:
                res[nome_autor] = res[nome_autor] + 1
            else:
                res[nome_autor] = 1
    
    top_20 = sorted(res.items(), key=lambda x: x[1], reverse=True)[:20]
    return dict(top_20)
    # Converter dicionário numa lista de tuplos de formato (nome do autor, nº de publicações)
    #   -> Organizar a lista em ordem decrescente de acordo com nº de publicações de cada autor
    #       -> Converter lista ordenada num dicionário

# Distribuição de Publicações Por Ano
def Distribuição_Ano(bd):

    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe a entrada no dicionário
            ano = data_pub.split('-')[0]
            if ano in res:
                res[ano] = res[ano] + 1
            else:
                res[ano] = 1
    return dict(sorted(res.items()))

# Distribuição de Publicações Por Mês em X Ano
def Distribuição_Mês(bd, x):

    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe a entrada no dicionário
            ano = data_pub.split('-')[0]
            mês = data_pub.split('-')[1]
            if x == ano:
                if mês in res:
                    res[mês] = res[mês] + 1
                else:
                    res[mês] = 1
    return dict(sorted(res.items()))

# Distribuição de Publicações de X Autor Por Ano
def Distribuição_Autor(bd, autor_nome):

    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe a entrada no dicionário
            for author in publicação.get('authors'):
                nome_autor = author.get('name').strip().lower()
                if autor_nome.strip().lower() == nome_autor:
                    ano = data_pub.split('-')[0]
                    if ano in res:
                        res[ano] = res[ano] + 1
                    else:
                        res[ano] = 1
    return dict(sorted(res.items()))

# Distribuição TOP 20 Palavras-Chave Mais Frequentes
def Distribuição_20PC(bd):

    res = {}
    for publicações in bd:
        palavras_chaves = publicações.get('keywords')
        if palavras_chaves: # Garante que existe a entrada no dicionário
            lista_palavras = palavras_chaves.split(',') # Criamos uma lista com as palavras-chave de cada publicação
            for pc in lista_palavras:
                pc = pc.strip(' .') # Retiramos espaços a mais e pontos finais
                if pc in res:
                    res[pc] = res[pc] + 1
                else:
                    res[pc] = 1

    top_20 = sorted(res.items(), key=lambda x: x[1], reverse=True)[:20]
    return dict(top_20)
    # Converter dicionário numa lista de tuplos de formato (palavra-chave, contagem)
    #   -> Organizar a lista em ordem decrescente de acordo com a contagem de cada palavra-chave
    #       -> Converter lista ordenada num dicionário

# Distribuição da Palavra-Chave Mais Frequente Por Ano (TOP 1)
def Distribuição_PC(bd):

    res = {}
    for publicações in bd:
        data_pub = publicações.get('publish_date')
        palavras_chaves = publicações.get('keywords')
        if data_pub and palavras_chaves: # Garante que existem as entradas no dicionário
            ano = data_pub.split('-')[0]
            lista_palavras = palavras_chaves.split(',')
            if ano not in res:
                res[ano] = {}
            for pc in lista_palavras:
                pc = pc.strip(' .') # Retiramos espaços a mais e pontos finais
                if pc in res[ano]:
                    res[ano][pc] = res[ano][pc] + 1
                else:
                    res[ano][pc] = 1

    # Res -> {Ano: {Palavra-Chave: Contagem}}

    pc_mais_frequente = {} # Dicionário terá a estrutura {Ano: Palavra-Chave Mais Frequente}
    for ano, pc in res.items():
        top_1 = sorted(pc.items(), key=lambda x: x[1], reverse=True)[:1]
        # Converter dicionário numa lista de tuplos de formato (palavra-chave, contagem)
        #   -> Organizar a lista em ordem decrescente de acordo com a contagem de cada palavra-chave
        #       -> Converter lista ordenada num dicionário

        if top_1:  # Garante que existe pelo menos uma palavra-chave no TOP 1
            pc_mais_frequente[ano] = top_1[0]

    return pc_mais_frequente
