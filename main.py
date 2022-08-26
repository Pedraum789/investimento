from urllib import request
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def transformColumnsToNumbers(data):
    
    #
    data['Cotação'] = pd.to_numeric(data['Cotação'].str.replace('.', '').str.replace(',','.'))
    
    #
    data['FFO Yield'] = pd.to_numeric( data['FFO Yield'].str.replace('.','').str.rstrip('%').str.replace(',', '.'), errors='coerce')
    
    # Porcentagem de ganho anual
    data['Dividend Yield'] = pd.to_numeric( data['Dividend Yield'].str.replace('.','').str.rstrip('%').str.replace(',', '.'), errors='coerce')
    
    # Porcentagem de ganho mensal
    data['Dividendo Mensal'] = ((1 + (data['Dividend Yield'] / 100)) ** (1/12) - 1) * 100
    
    # Preco da acao por valor do patrimonio liquido
    data['P/VP'] = pd.to_numeric( data['P/VP'] / 100)
    
    # Valor de Mercado
    data['Valor de Mercado'] = pd.to_numeric( data['Valor de Mercado'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    # Liquidez
    data['Liquidez'] = pd.to_numeric( data['Liquidez'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    # Quantidade de Imoveis
    data['Qtd de imóveis'] = pd.to_numeric( data['Qtd de imóveis'])
    
    # Preco por Metro Quadrado
    data['Preço do m2'] = pd.to_numeric( data['Preço do m2'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    # Aluguel por M2
    data['Aluguel por m2'] = pd.to_numeric( data['Aluguel por m2'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    data['Cap Rate'] = pd.to_numeric( data['Cap Rate'], errors='coerce')
    
    # O quanto esta alugado
    # Ex: Ele tem 100 lugares para alugar e 30 esta sem alugar, a vacancia vai ser de 30%
    data['Vacância Média'] = pd.to_numeric( data['Vacância Média'], errors='coerce')
    
    data = data.replace(np.nan, 0, regex=True)
    return data

def renameColumn(data):
    return data.rename(
        columns={'Cotação': 'cotacao',
                 'FFO Yield': 'ffo_yield',
                 'Dividend Yield':'dividend_yield',
                 'Dividendo Mensal':'dividendo_mensal',
                 'P/VP':'p_vp',
                 'Valor de Mercado':'valor_de_mercado',
                 'Liquidez':'liquidez',
                 'Qtd de imóveis':'qto_de_imoveis',
                 'Preço do m2':'preco_do_m2',
                 'Aluguel por m2':'aluguel_por_m2',
                 'Cap Rate':'cap_rate',
                 'Vacância Média':'vacancia_media'})
    
def filterPVP(data):
    return data.query("p_vp<1")

def filterLiquidez(data):
    return data.query("liquidez > 500000")

def filterValorMercado(data):
    return data.query("valor_de_mercado > 1000000000")

def filterQtdDeImoveis(data):
    return data.query("qto_de_imoveis == 0 | qto_de_imoveis >= 15")

def filterVacancia(data):
    return data.query("vacancia_media == 0")

def filterDividendoMensal(data):
    return data.query("dividendo_mensal >= 1.2")

def filters(data):
    data = filterLiquidez(data)
    data = filterPVP(data)
    data = filterValorMercado(data)
    data = filterQtdDeImoveis(data)
    data = filterVacancia(data)
    data = filterDividendoMensal(data)
    return data

def main():

    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    req = requests.get('https://fundamentus.com.br/fii_resultado.php', headers=headers)

    if req.status_code == 200:
        content = req.content
        soup = BeautifulSoup(content, 'html.parser')
        tabela = soup.find(name = 'table')
        table_str = str(tabela)
        df = pd.read_html(table_str)[0]
        df = transformColumnsToNumbers(df)
        df = renameColumn(df)
        df = filters(df)
        
        

'''
fig, ax = plt.subplots(1,1)
data=[[1,2,3],
      [5,6,7],
      [8,9,10]]
column_labels=["Column 1", "Column 2", "Column 3"]
ax.axis('tight')
ax.axis('off')
ax.table(cellText=data,colLabels=column_labels,loc="center")

plt.show()

'''

if __name__ == '__main__':
    main()