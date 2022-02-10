import pandas as pd
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright


def is_int(val):
    if val[5:6].isdigit() == True :
        return val[:6]
    else:
        return val[:5]
#python -m playwright install


def df_cleasing_all( df, carteira):
    if carteira == 'dividendos':
            df['Ticker'] = df.apply(lambda x :  is_int((x['Ticker / Empresa'])) , axis=1)
            df['Empresa'] = df.apply(lambda x :  str(x['Ticker / Empresa'])[len(is_int((x['Ticker / Empresa']))):-14] , axis=1) #nome certo
            df = df.drop(columns = ['Ticker / Empresa', 'Ativo'])
            df['Rank'] = df.apply(lambda x : int(float(x['Rank'])/10), axis=1 )
            return df[['Rank', 'Ticker', 'Empresa', 'Início', 'DY esperado',
                    'Alocação', 'Entrada (R$)', 'Preço atual (R$)', 'Preço teto (R$)',
                    'Rentabilidade', 'Viés', 'Origem']]
    elif carteira == 'valor':
        df['Ticker'] = df.apply(lambda x :  is_int((x['Ticker / Empresa'])) , axis=1)
        df['Empresa'] = df.apply(lambda x :  str(x['Ticker / Empresa'])[len(is_int((x['Ticker / Empresa']))):-14] , axis=1) #nome certo
        df = df.drop(columns = ['Ticker / Empresa', 'Ativo'])
        df['Rank'] = df.apply(lambda x : int(float(x['Rank'])/10), axis=1 )
        return df[['Rank', 'Ticker', 'Empresa', 'Início', 'Alocação',
                    'Entrada (R$)', 'Preço atual (R$)', 'Preço teto (R$)', 'Rentabilidade',
                    'Viés', 'Origem']]
    elif carteira == 'fiis':
        df['Ticker'] = df.apply(lambda x :  is_int((x['Ticker'])) , axis=1)
        #df['Empresa'] = tentar cruzar futuramente com a base das corretoras para trazer o nome do ticker ou fundo sei la
        df = df.rename(columns={'Preço de entrada ajustado (R$)': 'Entrada (R$)'})
        df['Rank'] = df.apply(lambda x : int(float(x['Rank'])/10), axis=1 )
        return df[['Rank', 'Ticker', 'Setor/Tipo', 'Início', 'Alocação', 'DY esperado',
                    'Entrada (R$)', 'Preço atual (R$)', 'Preço teto (R$)',
                    'Rentabilidade', 'Viés', 'Origem']]
    elif carteira == 'small-caps':
        df['Ticker'] = df.apply(lambda x :  is_int((x['Ticker / Empresa'])) , axis=1)
        df['Empresa'] = df.apply(lambda x :  str(x['Ticker / Empresa'])[len(is_int((x['Ticker / Empresa']))):-14] , axis=1) #nome certo
        df = df.drop(columns = ['Ticker / Empresa', 'Ativo'])
        df['Rank'] = df.apply(lambda x : int(float(x['Rank'])/10), axis=1 )
        return df[['Rank', 'Ticker', 'Empresa', 'Início', 'Alocação',
                    'Entrada (R$)', 'Preço atual (R$)', 'Preço teto (R$)', 'Rentabilidade',
                    'Viés', 'Origem']]
    else:
        try:
            df['Ticker'] = df.apply(lambda x :  is_int((x['Ticker / Empresa'])) , axis=1)
            df['Empresa'] = df.apply(lambda x :  str(x['Ticker / Empresa'])[len(is_int((x['Ticker / Empresa']))):-14] , axis=1) #nome certo
            df = df.drop(columns = ['Ticker / Empresa', 'Ativo'])
            df['Rank'] = df.apply(lambda x : int(float(x['Rank'])/10), axis=1 )
            return df[['Rank', 'Ticker', 'Empresa', 'Início', 'Alocação',
                        'Entrada (R$)', 'Preço atual (R$)', 'Preço teto (R$)', 'Rentabilidade',
                        'Viés', 'Origem']] 
        except:
             return df
             raise TypeError("Erro base não mapeada")


def cria_df( dataframe, nomearquivo, colunas, caminho = None ):
    if caminho == None:
        caminho =''
    nmArquivo = caminho + nomearquivo+'_sunocompilado.csv' 
    colunas_arquivo= colunas
    dfs = pd.read_html("<html><head></head><body>" + str(dataframe) +"</body></html>", thousands='.', decimal=',' )
    df = dfs[1]
    df = df.rename(columns = colunas_arquivo )
    df = df.iloc[1: , :]
    df = df.fillna(0)
    df['Início'] = df['Início'].astype(int).astype(str).str.zfill(8)
    df = df[df.Início != '00000000']
    df['Início'] = pd.to_datetime(df['Início'], format='%d%m%Y')
    df['Origem'] = nomearquivo
    df = df_cleasing_all(df, nomearquivo)
    df.to_csv(nmArquivo, mode='a', index=False, header =(not os.path.exists(caminho)) )
    print(nomearquivo)
    #print(df)

def scrappingSuno(pagina, usuario, senha ):
    with sync_playwright() as p:
           for x in pagina: 
            colunas = {}
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(x)
            page.fill('input#user_email', usuario)
            page.fill('input#user_password',senha)
            page.click('button[type=submit]')
            page.wait_for_load_state()  
            tabela = page.inner_html('div.ant-spin-nested-loading')
            soup = BeautifulSoup(tabela, 'html.parser')
            for y in range(0,len(soup.find_all('div', {'class': 'qNne44XPCMtX9rW76lrv'}))):
                colunas[y] = soup.find_all('div', {'class': 'qNne44XPCMtX9rW76lrv'})[y].get_text("|",strip=True).split("|")[0]
                
            #tratamento para tirar a variação diaria das tabelas, estava bagunçando os números
            while( str(soup.find('div', {'title': 'Variação diária'})) != 'None'):
                soup.find('div', {'title': 'Variação diária'}).decompose()
            cria_df(soup, x.split('/')[4], colunas  )
            page.close()
            
