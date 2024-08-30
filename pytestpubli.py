import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
import time
import re
import os
from PIL import Image
import pytest
import allure


# Crear la carpeta 'screenshots' si no existe
screenshots_folder = 'screenshots_publi'
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)

def get_next_screenshot_path(folder, base_filename):
    """Genera el siguiente nombre de archivo disponible con un número consecutivo."""
    i = 1
    while True:
        filename = f"{base_filename}_{i:03d}.png"
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            return path
        i += 1

def capture_full_page_screenshot(driver, file_path2):
    """Captura una captura de pantalla completa de la página, manejando el desplazamiento."""
    # Obtener el tamaño total de la página
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Establecer el tamaño de la ventana al tamaño total de la página
    driver.set_window_size(total_width, total_height)

    # Tomar la captura de pantalla
    driver.save_screenshot(file_path2)
    #print(f'Captura de pantalla completa guardada en {file_path}')

def capture_element_screenshot(driver, element, file_path):
    """Captura una captura de pantalla de un elemento específico, manejando el desplazamiento."""
    # Obtener la ubicación y el tamaño del elemento
    location = element.location
    size = element.size

    # Tomar la captura de pantalla de toda la página
    screenshot_path = 'temp_screenshot.png'
    driver.save_screenshot(screenshot_path)

    # Abrir la captura de pantalla y recortar el área del elemento
    image = Image.open(screenshot_path)
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    image = image.crop((left, top, right, bottom))
    image.save(file_path)
    if os.path.exists(screenshot_path):
            os.remove(screenshot_path)  # Eliminar el archivo temporal
    #print(f'Captura de pantalla del elemento guardada en {file_path}')

@pytest.fixture
def setup():
    # Configurar el controlador de Chrome
    chromedriver_autoinstaller.install() 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("Versión chromedriver:", driver.capabilities['browserVersion'])
    driver.maximize_window()

    # URL de la página que deseas validar
    url = 'https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura'
    driver.get(url)

    # Espera a que la página cargue completamente
    driver.implicitly_wait(10)
    
    yield driver  # Retorna el driver para usarlo en las pruebas
    
    driver.quit()  # Asegúrate de cerrar el navegador después de la prueba

@pytest.fixture
def df():
    # Cargar tu DataFrame aquí
    # Por ejemplo:
    import pandas as pd
    # Leer el archivo CSV en un DataFrame
    csv_path = '/var/jenkins_home/workspace/Publicacion/Archivos/PRES_2024.csv'
    df = pd.read_csv(csv_path, skiprows=3, nrows=1, header=None, names=["ACTAS_ESPERADAS","ACTAS_REGISTRADAS","ACTAS_FUERA_CATALOGO","ACTAS_CAPTURADAS","PORCENTAJE_ACTAS_CAPTURADAS","ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_INCONSISTENCIAS","ACTAS_NO_CONTABILIZADAS","LISTA_NOMINAL_ACTAS_CONTABILIZADAS","TOTAL_VOTOS_C_CS","TOTAL_VOTOS_S_CS","PORCENTAJE_PARTICIPACION_CIUDADANA"])

    # Mapeo de las columnas conteos
    ACTAS_ESPERADAS = 'ACTAS_ESPERADAS'
    ACTAS_REGISTRADAS = 'ACTAS_REGISTRADAS'
    ACTAS_FUERA_CATALOGO = 'ACTAS_FUERA_CATALOGO'
    ACTAS_CAPTURADAS = 'ACTAS_CAPTURADAS'
    PORCENTAJE_ACTAS_CAPTURADAS = 'PORCENTAJE_ACTAS_CAPTURADAS'
    ACTAS_CONTABILIZADAS = 'ACTAS_CONTABILIZADAS'
    PORCENTAJE_ACTAS_CONTABILIZADAS = 'PORCENTAJE_ACTAS_CONTABILIZADAS'
    PORCENTAJE_ACTAS_INCONSISTENCIAS = 'PORCENTAJE_ACTAS_INCONSISTENCIAS'
    ACTAS_NO_CONTABILIZADAS = 'ACTAS_NO_CONTABILIZADAS'
    LISTA_NOMINAL_ACTAS_CONTABILIZADAS = 'LISTA_NOMINAL_ACTAS_CONTABILIZADAS'
    TOTAL_VOTOS_C_CS = 'TOTAL_VOTOS_C_CS'
    TOTAL_VOTOS_S_CS = 'TOTAL_VOTOS_S_CS'
    PORCENTAJE_PARTICIPACION_CIUDADANA = 'PORCENTAJE_PARTICIPACION_CIUDADANA'
    return pd.DataFrame(df)

@pytest.fixture
def screenshots_folder():
    # Define la ruta de la carpeta donde almacenarás las capturas de pantalla
    return "screenshots_publi"

@allure.feature('Validación de datos en sitio de Publicación - 2')
@allure.story('1.- Validación de número de actas esperadas en Estadística Nacional')
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_esperadas_estadistica_nacional_coinciden(setup, df, screenshots_folder):
    valor_con_comas2 = "{:,.0f}".format(int("".join(str(x) for x in df['ACTAS_ESPERADAS'].astype(int).values)))

    driver = setup
    elemento3 = driver.find_element(By.XPATH, "/html/body/app-root/app-federal/div/div/div[3]/app-nacional/div/app-estadistica/div[1]/div[1]/div[2]/div[1]/p[1]/strong")
    valor_en_pagina3 = elemento3.text

    file_path = get_next_screenshot_path(screenshots_folder, 'actas_esperadas')
    capture_element_screenshot(driver, elemento3, file_path)

    file_path2 = get_next_screenshot_path(screenshots_folder, 'pagina_completa')
    capture_full_page_screenshot(driver, file_path2)
    
    with allure.step("Comparando los valores de sitio vs csv"):
        if valor_en_pagina3 == valor_con_comas2:
            allure.attach(
                f"1.- Los valores coinciden, Sitio: {valor_en_pagina3} CSV: {valor_con_comas2}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
            with open(file_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Captura de pantalla del elemento",
                    attachment_type=allure.attachment_type.PNG
                )
            with open(file_path2, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Captura de pantalla completa",
                    attachment_type=allure.attachment_type.PNG
                )
        else:
            allure.attach(
                f"1.- Los valores no coinciden, Sitio: {valor_en_pagina3} CSV: {valor_con_comas2}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
            with open(file_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Captura de pantalla del error",
                    attachment_type=allure.attachment_type.PNG
                )
            with open(file_path2, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Captura de pantalla completa",
                    attachment_type=allure.attachment_type.PNG
                )
        assert valor_en_pagina3 == valor_con_comas2, (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )