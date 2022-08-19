from urllib import request
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def transformColumnsToNumbers(data):
    
    data['Cotação'] = pd.to_numeric(data['Cotação'].str.replace('.', '').str.replace(',','.'))
    
    data['FFO Yield'] = pd.to_numeric( data['FFO Yield'].str.replace('.','').str.rstrip('%').str.replace(',', '.'), errors='coerce')
    
    data['Dividend Yield'] = pd.to_numeric( data['Dividend Yield'].str.replace('.','').str.rstrip('%').str.replace(',', '.'), errors='coerce')
    # Porcentagem de ganho mensal
    data['Dividendo Mensal'] = ((1 + (data['Dividend Yield'] / 100)) ** (1/12) - 1) * 100
    
    data['P/VP'] = pd.to_numeric( data['P/VP'])
    #Valor de Mercado
    data['Valor de Mercado'] = pd.to_numeric( data['Valor de Mercado'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    data['Liquidez'] = pd.to_numeric( data['Liquidez'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    #Quantidade de Imoveis
    data['Qtd de imóveis'] = pd.to_numeric( data['Qtd de imóveis'])
    #Preco por Metro Quadrado
    data['Preço do m2'] = pd.to_numeric( data['Preço do m2'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    data['Aluguel por m2'] = pd.to_numeric( data['Aluguel por m2'].str.replace('.','').str.replace(',', '.'), errors='coerce')
    
    data['Cap Rate'] = pd.to_numeric( data['Cap Rate'], errors='coerce')
    # O quanto esta alugado
    # Ex: Ele tem 100 lugares para alugar e 30 esta sem alugar, a vacancia vai ser de 30%
    data['Vacância Média'] = pd.to_numeric( data['Vacância Média'], errors='coerce')
    
    data = data.replace(np.nan, 0, regex=True)
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
    
if __name__ == '__main__':
    main()