import smtplib
import email.message
import datetime
import pandas as pd
!pip install translate
from translate import Translator
!pip install gspread oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

def Scraping_cbc(limit=20):
    site_cbc = requests.get('https://www.cbc.ca/news/world/')
    bs = BeautifulSoup(site_cbc.content,'html.parser')

    noticias = bs.find_all('section', 'featuredArea sclt-featuredarea')
    ultimas_noticias = []
    for n in noticias:
        info = 'CBC News (Canadá, Toronto, Ontário) - Inglês - Traduzido'
        Link = n.find('a')['href']
        Manchete = n.find('h3').text
        
        # traduzindo a manchete para português
        translator= Translator(to_lang="pt")
        Manchete = translator.translate(Manchete)
        
        Data = n.find('time')['datetime']
        ultimas_noticias.append({'Manchete': Manchete, 'Link': Link, 'Data': Data, 'Informações':info})

    ultimas_folha = pd.DataFrame(ultimas_noticias)
    return ultimas_folha

app = Flask(__name__)

@app.route("/")
def index():
    return "Bem-vindo ao Web Scraper!"

@app.route("/cbc")
def cbc():
    noticias = Scraping_cbc()
    return render_template("noticias.html", noticias=noticias)

@app.route("/thetimes")
def thetimes():
    noticias = Scraping_thetimes()
    return render_template("noticias.html", noticias=noticias)

@app.route("/folha")
def folha():
    noticias = Scraping_folha()
    return render_template("noticias.html", noticias=noticias)

@app.route("/elpais")
def elpais():
    noticias = Scraping_ElPais()
    return render_template("noticias.html", noticias=noticias)

@app.route("/bbc")
def bbc():
    noticias = Scraping_BBC()
    return render_template("noticias.html", noticias=noticias)
