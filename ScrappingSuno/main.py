import  getpass
from processos import *
import pandas as pd

usr = input('Digite o usuario: ')
pwrd =   getpass.getpass('Digite a Senha:')

#Atualmente o programa apenas importa carteiras de Valor, Small-Caps, FII e dividendos.

scrappingSuno(['https://investidor.suno.com.br/carteiras/valor','https://investidor.suno.com.br/carteiras/small-caps','https://investidor.suno.com.br/carteiras/fiis','https://investidor.suno.com.br/carteiras/dividendos'], usr, pwrd)

#df_dividendos =pd.read_csv("dividendos_sunocompilado.csv")
#df_fii = pd.read_csv('fiis_sunocompilado.csv')
#df_small = pd.read_csv('small-caps_sunocompilado.csv')
#df_valor = pd.read_csv('valor_sunocompilado.csv')


#print(df)

