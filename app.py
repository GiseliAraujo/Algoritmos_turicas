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
def Scraping_thetimes(limit=20):
    site_thetimes = requests.get('https://www.nytimes.com/spotlight/dispatches-international')
    bs = BeautifulSoup(site_thetimes.content,'html.parser')

    noticias = bs.find_all('li', 'css-112uytv')
    ultimas_noticias = []
    for n in noticias:
        info = 'The New York Times (Estados Unidos, Nova Iorque, Nova Iorque) - Inglês'
        Link = n.find('a')['href']
        Manchete = n.find('h2').text
        
        # traduzindo a manchete para português
        translator= Translator(to_lang="pt")
        Manchete = translator.translate(Manchete)
        
        Data = ""
        ultimas_noticias.append({'Manchete': Manchete, 'Link': Link, 'Data': Data, 'Informações':info})

    ultimas_thetimes = pd.DataFrame(ultimas_noticias)
    return ultimas_thetimes


def Scraping_folha(limit=20):
    site_Folha = requests.get('https://www1.folha.uol.com.br/ultimas-noticias/')
    bs = BeautifulSoup(site_Folha.content,'html.parser')

    noticias = bs.find_all('div', 'c-headline__content')
    ultimas_noticias = []
    for n in noticias:
        info = 'Folha de S.Paulo (Brasil, São Paulo, São Paulo) - Português'
        Link = n.find('a')['href']
        Manchete = n.find('h2').text
        Data = n.find('time')['datetime']
        ultimas_noticias.append({'Manchete': Manchete, 'Link': Link, 'Data': Data, 'Informações':info})


    ultimas_folha = pd.DataFrame(ultimas_noticias[-limit:])
    return ultimas_folha

def Scraping_ElPais(limit=20):
    site_elpais = requests.get('https://brasil.elpais.com/lomasvisto/index.html')
    bs = BeautifulSoup(site_elpais.content,'html.parser')

    noticias = bs.find_all('div',{'class':'modulo estirar'})
    ultimas_noticias = []
    for n in noticias[:20]:
        info = 'El Pais'
        Link = n.find('h2').find('a').get('href')
        manchete = n.find('h2').find('a').text
        Data =(datetime.datetime.now()).strftime('%Y-%m-%d')
        ultimas_noticias.append({'Manchete': manchete, 'Link': Link, 'Data': Data, 'Informações':info})


    ultimas_elpais = pd.DataFrame(ultimas_noticias)
    return ultimas_elpais

def enviar_email():
        noticias_cbc = Scraping_cbc()
        noticias_thetimes = Scraping_thetimes()
        noticias_folha = Scraping_folha()
        noticias_elpais = Scraping_ElPais()
        #noticias_bbc = Scraping_BBC

        data_atual = datetime.date.today()
        corpo_email = f"""
        <p style="color: red">América do Norte:</p>
        <p>Data/hora de geração do email: <b>{data_atual}</b>.</p>
        <p>Noticias CBC</p>
        <ul>
        """
        for item in noticias_cbc.itertuples():
            corpo_email += f"<li><a href='{item.Link}'>{item.Manchete}</a> ({item.Data}) - {item.Informações}</li>"
        corpo_email += "</ul>"

        corpo_email += f"""
        <p>Noticias The Times</p>
        <ul>
        """
        for item in noticias_thetimes.itertuples():
            corpo_email += f"<li><a href='{item.Link}'>{item.Manchete}</a> ({item.Data}) - {item.Informações}</li>"
        corpo_email += "</ul>"

        corpo_email += f"""
        <p style="color: red">América do Sul:</p>
        <p>Noticias Folha de São Paulo</p>
        <ul>
        """
        for item in noticias_folha.itertuples():
            corpo_email += f"<li><a href='{item.Link}'>{item.Manchete}</a> ({item.Data}) - {item.Informações}</li>"
        corpo_email += "</ul>"

        corpo_email += f"""
        <p>Noticias El Pais</p>
        <ul>
        """
        for item in noticias_elpais.itertuples():
            corpo_email += f"<li><a href='{item.Link}'>{item.Manchete}</a> ({item.Data}) - {item.Informações}</li>"
        corpo_email += "</ul>" 

        
        msg = email.message.Message()
        msg['Subject'] = "Assunto"
        msg['From'] = 'giselialmeidadearaujo@gmail.com'
        msg['To'] = 'giselialmeidadearaujo@gmail.com'
        password =  KEY_GMAIL
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
app = Flask(__name__)

@app.route("/")
def index():
    return "Bem-vindo ao Web Scraper!"

@app.route("/cbc")
def cbc():
    noticias = Scraping_cbc()
    return '<!doctype html>
                    <html>
                        <head>
                            <title>Resultado</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Manchete</th>
                                    <th>Link</th>
                                    <th>Data</th>
                                    <th>Informações</th>
                                </tr>
                                {% for row in noticias.iterrows() %}
                                <tr>
                                    <td>{{ row[1]['Manchete'] }}</td>
                                    <td>{{ row[1]['Link'] }}</td>
                                    <td>{{ row[1]['Data'] }}</td>
                                    <td>{{ row[1]['Informações'] }}</td>
                                </tr>
                                {% endfor %}
                            </table>
                        </body>
                    </html>'

@app.route("/thetimes")
def thetimes():
    noticias = Scraping_thetimes()
    return '<!doctype html>
                    <html>
                        <head>
                            <title>Resultado</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Manchete</th>
                                    <th>Link</th>
                                    <th>Data</th>
                                    <th>Informações</th>
                                </tr>
                                {% for row in noticias.iterrows() %}
                                <tr>
                                    <td>{{ row[1]['Manchete'] }}</td>
                                    <td>{{ row[1]['Link'] }}</td>
                                    <td>{{ row[1]['Data'] }}</td>
                                    <td>{{ row[1]['Informações'] }}</td>
                                </tr>
                                {% endfor %}
                            </table>
                        </body>
                    </html>'

@app.route("/folha")
def folha():
    noticias = Scraping_folha()
    return '<!doctype html>
                    <html>
                        <head>
                            <title>Resultado</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Manchete</th>
                                    <th>Link</th>
                                    <th>Data</th>
                                    <th>Informações</th>
                                </tr>
                                {% for row in noticias.iterrows() %}
                                <tr>
                                    <td>{{ row[1]['Manchete'] }}</td>
                                    <td>{{ row[1]['Link'] }}</td>
                                    <td>{{ row[1]['Data'] }}</td>
                                    <td>{{ row[1]['Informações'] }}</td>
                                </tr>
                                {% endfor %}
                            </table>
                        </body>
                    </html>'

@app.route("/elpais")
def elpais():
    noticias = Scraping_ElPais()
    return '<!doctype html>
                    <html>
                        <head>
                            <title>Resultado</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Manchete</th>
                                    <th>Link</th>
                                    <th>Data</th>
                                    <th>Informações</th>
                                </tr>
                                {% for row in noticias.iterrows() %}
                                <tr>
                                    <td>{{ row[1]['Manchete'] }}</td>
                                    <td>{{ row[1]['Link'] }}</td>
                                    <td>{{ row[1]['Data'] }}</td>
                                    <td>{{ row[1]['Informações'] }}</td>
                                </tr>
                                {% endfor %}
                            </table>
                        </body>
                    </html>'

@app.route("/bbc")
def bbc():
    noticias = Scraping_BBC()
    return '<!doctype html>
                    <html>
                        <head>
                            <title>Resultado</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Manchete</th>
                                    <th>Link</th>
                                    <th>Data</th>
                                    <th>Informações</th>
                                </tr>
                                {% for row in noticias.iterrows() %}
                                <tr>
                                    <td>{{ row[1]['Manchete'] }}</td>
                                    <td>{{ row[1]['Link'] }}</td>
                                    <td>{{ row[1]['Data'] }}</td>
                                    <td>{{ row[1]['Informações'] }}</td>
                                </tr>
                                {% endfor %}
                            </table>
                        </body>
                    </html>'
