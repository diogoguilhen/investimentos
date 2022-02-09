import  getpass
from processos import *


usr = input('Digite o usuario: ')
pwrd =   getpass.getpass('Digite a Senha:')

#Atualmente o programa apenas importa carteiras de Valor, Small-Caps, FII e dividendos.

scrappingSuno(['https://investidor.suno.com.br/carteiras/valor','https://investidor.suno.com.br/carteiras/small-caps','https://investidor.suno.com.br/carteiras/fiis','https://investidor.suno.com.br/carteiras/dividendos'], usr, pwrd)

