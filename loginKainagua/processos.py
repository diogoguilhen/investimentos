import pandas as pd
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright
import time

def agendamentoAula(pagina, usuario, senha ):
    with sync_playwright() as p:
           for x in pagina: 
            colunas = {}
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(x)
            page.wait_for_load_state() 
            page.fill('input#loginUsuario', usuario)
            page.fill('input#senhaUsuario',senha)
            page.get_by_role("button", name="Entrar").click()
            page.wait_for_load_state() 
            page.get_by_role("link", name=" Reserva de Aulas").click()
            page.wait_for_load_state() 
            page.get_by_role("button", name="#NATAÇÃO ADULTO").click()
            page.wait_for_load_state() 
            page.get_by_role("button", name="").click()
            page.wait_for_load_state() 
            page.get_by_role("button", name="NAT 138 NATAÇÃO ADULTO 06:00/07:00 hs SERGIO AUGUSTO DE SOUZA ").click()
            page.wait_for_load_state() 
            page.once("dialog", lambda dialog: dialog.dismiss())
            page.get_by_role("button", name="Reservar").click()
            page.close()
            


