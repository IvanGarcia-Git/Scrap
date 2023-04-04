from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import date
import pymysql
import os


def main():

    ################################
    # Conexión a la Base de Datos: #
    ################################

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="easyland"
    )
    mycursor = connection.cursor()

    ################################
    # Bucle para scrapear paginas: #
    ################################

    for i in range(10): # Aumentar numero de Range para scrapear mucho mas contenido
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.youtube.com/results?search_query=among+us+español&sp=EgIQAQ%253D%253D"+"&page="+str(i)) # URL de la pagina a scrapear
        # Estructura del contenido:
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        # Scraping de contenido:
        titles = soup.findAll('a',id='video-title')
        descripciones = soup.findAll('yt-formatted-string',class_='ytd-channel-name')
        urls = soup.findAll()
        video_urls = soup.findAll('a',id='video-title')
        url_imagen = soup.findAll('img',class_='yt-img-shadow',width='360')
        url_imagen_canal = soup.findAll('img',class_='yt-img-shadow',width='24')
        descripcion_post = soup.findAll('yt-formatted-string',id='description-text')
        # Variables:
        i = 0
        j = 0
        # Variables para introducir la fecha:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        # Recorrer todo:
        for title in titles:
            urlvideo = 'https://youtube.com'+video_urls[j].get('href')
            sql = "INSERT IGNORE INTO yt(id_post,post_titulo,post_nombre_canal,post_video_url,post_img_url,fecha_post,post_img_canal,descripcion_post) VALUES('','{}','{}','{}','{}','{}','{}','{}')".format(title.text,descripciones[i].text,urlvideo,url_imagen[j].get('src'),d1,url_imagen_canal[j].get('src'),descripcion_post[j])
            mycursor.execute(sql)
            connection.commit()

            i+=2
            j+=1
main()
