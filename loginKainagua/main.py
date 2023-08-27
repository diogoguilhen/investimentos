import  getpass
from processos import *
import pandas as pd
 
usr = input('Digite o usuario: ')
pwrd =   getpass.getpass('Digite a Senha:')
 
 
agendamentoAula(['https://infoskyweb.com.br/moduloweb/reservaAulas.jsp?key=05f903d55f0bc62e3dafc540c6be228fcfb83f5f'], usr, pwrd)
 