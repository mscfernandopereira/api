# Consulta as parcelas do Bolsa Família Disponível dos Beneficiários por Município e Mes/Ano
# Municipio Coruripe - código IBGE 2702306 | Mes/Ano - 2013.01

import requests
import pandas as pd

def obter_dados_api(mes_ano, codigo_ibge):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/bolsa-familia-disponivel-beneficiario-por-municipio"
    chave_api = "" # coloque sua chave-api aqui

    params = {"mesAno": mes_ano, "codigoIbge": codigo_ibge, "pagina": 1}
    headers = {"accept": "*/*", "chave-api-dados": chave_api}

    dados_paginas = []

    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            dados_json = response.json()

            if not dados_json:
                break

            dados_paginas.extend(dados_json)
            params["pagina"] += 1

        except requests.exceptions.RequestException as e:
            print("Erro ao fazer a requisição:", e)
            break

    return dados_paginas

def criar_dataframe():
    mes_ano = 201301 # mês de referência AAAAMM
    codigo_ibge = "2702306" # código IBGE do município | Coruripe-AL 2702306

    dados_bolsaFamilia = obter_dados_api(mes_ano, codigo_ibge)

    if dados_bolsaFamilia:
        df = pd.DataFrame(dados_bolsaFamilia)
        return df
    else:
        return None

if __name__ == "__main__":
    df = criar_dataframe()
    

# Normalizando as colunas que contem dicionario de dados
titular_df = pd.json_normalize(df['titularBolsaFamilia'])

# Concatenar o DataFrame original (df) com o DataFrame da coluna titular
df_normalizado = pd.concat([df, titular_df], axis=1) # concatena os dataframes
df_normalizado.drop(['id', 'dataMesCompetencia', 'titularBolsaFamilia', 'municipio'], axis=1, inplace=True) # exclui colunas

# transforma o dataframe 'titular_df' em um arquivo CSV
nome_do_arquivo = 'bolsa_familia_.csv'
df_normalizado.to_csv(nome_do_arquivo, index=False, encoding='utf-8')
