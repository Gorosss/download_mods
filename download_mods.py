import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Ruta al controlador de ChromeDriver
chromedriver_path = 'C:/Users/jongo/Downloads/chromedriver-win64/chromedriver.exe'  # Cambia esto a la ruta de tu chromedriver

# Configuración de las opciones de Chrome
options = ChromeOptions()
prefs = {'download.default_directory': os.path.abspath('mods_downloads')}
options.add_experimental_option('prefs', {
    "download.default_directory": os.path.abspath("mods_downloads"),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
service = ChromeService(executable_path=chromedriver_path)

# Crear un directorio de descargas si no existe
os.makedirs('mods_downloads', exist_ok=True)

download_directory = 'mods_downloads'


# Inicializar el navegador
driver = webdriver.Chrome(service=service, options=options)

# Leer el archivo HTML
with open('modlist.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Encontrar todos los enlaces a CurseForge
links = soup.find_all('a', href=True)
curseforge_links = [link['href'] for link in links if 'curseforge.com/minecraft/mc-mods/' in link['href']]

# Versión objetivo
target_version = '1.20.1'
target_loader = 'Fabric'

# Iterar sobre cada enlace y descargar el mod compatible con la versión deseada
for mod_link in curseforge_links:

    print(f"Descargando: {mod_link}")

    try:
        driver.get(mod_link)
        


        # Esperar hasta que el botón de descarga (Files) esté presente y clic en él
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-cta.download-cta'))
        )

        print(f"Download loaded")

         # Hacer clic en el botón de descarga que abre el pop-up
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-cta.download-cta'))
        ).click()

        print(f"Download click")


         # Esperar a que el pop-up sea visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.modal-container'))
        )

        print(f"pop-up loaded")

         # Abrir el menú desplegable para seleccionar la versión
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.select-dropdown .dropdown'))
        )
        dropdown.click()

        print(f"dropdown.click version")

        # Esperar y seleccionar la opción de versión
        
        version_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{target_version}')]"))
        )
        version_option.click()


        print(f"Version {target_version} selected")


         # Abrir el menú desplegable para seleccionar del loader
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.select-dropdown:nth-of-type(2) .dropdown'))
        )
        dropdown.click()

        print(f"dropdown.click loader")

        # Esperar y seleccionar la opción del loader
        
        version_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{target_loader}')]"))
        )
        version_option.click()

        time.sleep(5)

        print(f"Version {target_loader} selected")








        file_card = driver.find_elements(By.CSS_SELECTOR, 'a.file-card')

        #print(file_card)

        relative_url = file_card[0].get_attribute('href')

        print(relative_url)

        download_url = relative_url.replace('/files/', '/download/')

        print(download_url)


         # Navegar al enlace de descarga para gestionar la espera
        driver.get(download_url)

        # Esperar el tiempo necesario (6 segundos)
        time.sleep(6)

        # Esperar a que el navegador redirija al enlace de descarga final
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Puedes usar un elemento específico si es necesario
        )

        # Obtener la URL final después de la redirección
        final_url = driver.current_url
        print(f"Final Download URL: {final_url}")

        # Descargar el archivo usando requests
        response = requests.get(final_url, stream=True)
        filename = final_url.split('/')[-1]  # Extraer el nombre del archivo del enlace

        # Ruta completa para guardar el archivo
        file_path = os.path.join(download_directory, filename)
        
        print(f"Descargado: {filename} en {download_directory}")

    except Exception as e:
        print(f"Error al procesar {mod_link}: {e}")

# Cerrar el navegador
driver.quit()
