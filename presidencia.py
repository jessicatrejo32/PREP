import pandas as pd
import numpy as np
from rich import print
import re
import datetime
import pytest
import allure

def registrar_hora():
    ahora = datetime.datetime.now()
    hora_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    print("Hora de ejecución:", hora_formateada)

file_path = '/var/jenkins_home/workspace/Publicacion/Archivos/PRES_2024.csv'
df = pd.read_csv(file_path, skiprows=4, delimiter=',', low_memory=False)  # Cambia ';' por el delimitador correcto
df1 = pd.read_csv(file_path, skiprows=3, nrows=1, header=None, names=["ACTAS_ESPERADAS","ACTAS_REGISTRADAS","ACTAS_FUERA_CATALOGO","ACTAS_CAPTURADAS","PORCENTAJE_ACTAS_CAPTURADAS","ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_INCONSISTENCIAS","ACTAS_NO_CONTABILIZADAS","LISTA_NOMINAL_ACTAS_CONTABILIZADAS","TOTAL_VOTOS_C_CS","TOTAL_VOTOS_S_CS","PORCENTAJE_PARTICIPACION_CIUDADANA"])

# Mapeo de las columnas datos
CONTABILIZADA = 'CONTABILIZADA'
OBSERVACIONES = 'OBSERVACIONES'
LISTA_NOMINAL = 'LISTA_NOMINAL'
TOTAL_VOTOS_CALCULADO = 'TOTAL_VOTOS_CALCULADO'
TIPO_CASILLA = 'TIPO_CASILLA'

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

# Función para limpiar los valores
def limpiar_valor(valor):
    # Usar regex para extraer solo el contenido entre corchetes y comillas simples
    if isinstance(valor, str):
        # Extrae el contenido entre comillas simples
        return ', '.join(re.findall(r"'([^']*)'", valor))
    return valor
# Aplicar la limpieza a la columna
df[OBSERVACIONES] = df[OBSERVACIONES].apply(limpiar_valor)

# Filtros para realizar conteos y enviarlos como parametros
valores_especificos = ['1']
valores_especificos2 = ['2']
valores_especificos3 = ['0']
valores_especificos4 = ['0','1','2']
valores_especificos5 = ['0','1']
valores_especificos6 = [
    'Todos los campos ilegibles',
    'Sin dato',
    'Ilegible',
    'Todos los campos vacíos',
    'Ilegible, Sin dato',
    'Excede Lista Nominal',
    'Excede Lista Nominal, Sin dato',
    'Excede Lista Nominal, Ilegible',
    'Excede Lista Nominal, Ilegible, Sin dato'
]

if CONTABILIZADA in df.columns:
    filtro = df[CONTABILIZADA].isin(valores_especificos)
    df_filtrado = df[filtro]

if CONTABILIZADA in df.columns:
    filtro2 = df[CONTABILIZADA].isin(valores_especificos2)
    df_filtrado2 = df[filtro2]

if CONTABILIZADA in df.columns:
    filtro3 = df[CONTABILIZADA].isin(valores_especificos3)
    df_filtrado3 = df[filtro3]

if CONTABILIZADA in df.columns:
    filtro4 = df[CONTABILIZADA].isin(valores_especificos4)
    df_filtrado4 = df[filtro4]

if CONTABILIZADA in df.columns:
    filtro5 = df[CONTABILIZADA].isin(valores_especificos5)
    df_filtrado5 = df[filtro5]

if OBSERVACIONES in df.columns:
    filtro6 = df[OBSERVACIONES].isin(valores_especificos6)
    df_filtrado6 = df[filtro6]

if CONTABILIZADA in df.columns and LISTA_NOMINAL in df.columns:
    df_filtrado7 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado7[LISTA_NOMINAL] = pd.to_numeric(df_filtrado[LISTA_NOMINAL], errors='coerce')
    
if CONTABILIZADA in df.columns and TOTAL_VOTOS_CALCULADO in df.columns:
    df_filtrado8 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado8[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado[TOTAL_VOTOS_CALCULADO], errors='coerce')

if TOTAL_VOTOS_CALCULADO in df.columns and TIPO_CASILLA in df.columns:
    #df_filtrado9 = df[df[TIPO_CASILLA] != 'S'].copy()
    df_filtrado9 = df[(df[CONTABILIZADA].isin(['1','2'])) & (df[TIPO_CASILLA] != 'S')].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado9[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado9[TOTAL_VOTOS_CALCULADO], errors='coerce')

    value_counts = df_filtrado[CONTABILIZADA].value_counts()
    value_counts1 = df_filtrado2[CONTABILIZADA].value_counts()
    value_counts2 = df_filtrado3[CONTABILIZADA].value_counts()
    value_counts3 = df_filtrado4[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts3 = [value_counts3]
    value_counts4 = df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts4 = [value_counts4]
    value_counts5 = (df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts5 = pd.Series(value_counts5)
    value_counts5 = value_counts5.apply(lambda x: int(x * 10000) / 10000)
    value_counts6 = (df_filtrado[CONTABILIZADA].value_counts() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts6 = pd.Series(value_counts6)
    value_counts6 = value_counts6.apply(lambda x: int(x * 10000) / 10000)
    value_counts7 = (df_filtrado6[OBSERVACIONES].value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts7 = pd.Series(value_counts7)
    value_counts7 = value_counts7.apply(lambda x: int(x * 10000) / 10000)
    value_counts8 = df_filtrado7[LISTA_NOMINAL].sum()
    value_counts8 = [value_counts8]
    value_counts9 = (df_filtrado8[TOTAL_VOTOS_CALCULADO].sum() * 100) / value_counts8
    value_counts9 = pd.Series(value_counts9)
    value_counts9 = value_counts9.apply(lambda x: int(x * 10000) / 10000)
    value_counts10 = df_filtrado8[TOTAL_VOTOS_CALCULADO].sum()
    value_counts10 = [value_counts10]
    value_counts11 = df_filtrado9[TOTAL_VOTOS_CALCULADO].sum()
    value_counts11 = [value_counts11]
    actas_regis = df1[ACTAS_REGISTRADAS].values
    actas_fuera = df1[ACTAS_FUERA_CATALOGO].values
    actas_cap = df1[ACTAS_CAPTURADAS].values
    actas_cap_por = df1[PORCENTAJE_ACTAS_CAPTURADAS].values
    actas_con = df1[ACTAS_CONTABILIZADAS].values
    actas_con_por = df1[PORCENTAJE_ACTAS_CONTABILIZADAS].values
    actas_incon_por = df1[PORCENTAJE_ACTAS_INCONSISTENCIAS].values
    actas_nocon = df1[ACTAS_NO_CONTABILIZADAS].values
    lnactascon = df1[LISTA_NOMINAL_ACTAS_CONTABILIZADAS].values
    totalvotosc = df1[TOTAL_VOTOS_C_CS].values
    totalvotoss = df1[TOTAL_VOTOS_S_CS].values
    participacionciu = df1[PORCENTAJE_PARTICIPACION_CIUDADANA].values
    #print(value_counts11)

print("VALIDACION DE CSV DE PRESIDENCIA, REALIZANDO CONTEOS CON LOS DATOS Y VALIDANDO CON EL PRIMER ENCABEZADO")

registrar_hora()
print("Archivo:", file_path)

print("1.- ACTAS_ESPERADAS:", df1[ACTAS_ESPERADAS].values)

if np.array_equal(value_counts3, actas_regis):
    print("[green]2.- Los valores de ACTAS_REGISTRADAS coinciden:[/green]", actas_regis)
else:
    print("[red]2.- Los valores de ACTAS_REGISTRADAS no coinciden.[/red]", actas_regis, "vs", value_counts3)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('2.- Validación de Actas Registradas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_registradas_coinciden():
    """
    Prueba que los valores de ACTAS_REGISTRADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_REGISTRADAS con los esperados"):
        if np.array_equal(value_counts3, actas_regis):
            allure.attach(
                f"2.- Los valores de ACTAS_REGISTRADAS coinciden: {actas_regis}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"2.- Los valores de ACTAS_REGISTRADAS no coinciden. {actas_regis} vs {value_counts3}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts3, actas_regis), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts1, actas_fuera):
    print("[green]3.- Los valores de ACTAS_FUERA_CATALOGO coinciden:[/green]", actas_fuera)
else:
    print("[red]3.- Los valores de ACTAS_FUERA_CATALOGO no coinciden.[/red]", actas_fuera)
    print(value_counts1)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('3.- Validación de Actas Fuera de Catálogo')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_fuera_catalogo_coinciden():
    """
    Prueba que los valores de ACTAS_FUERA_CATALOGO coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_FUERA_CATALOGO con los esperados"):
        if np.array_equal(value_counts1, actas_fuera):
            allure.attach(
                f"3.- Los valores de ACTAS_FUERA_CATALOGO coinciden: {actas_fuera}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"3.- Los valores de ACTAS_FUERA_CATALOGO no coinciden. {actas_fuera} vs {value_counts1}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts1, actas_fuera), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts4, actas_cap):
    print("[green]4.- Los valores de ACTAS_CAPTURADAS coinciden:[/green]", actas_cap)
else:
    print("[red]4.- Los valores de ACTAS_CAPTURADAS no coinciden.[/red]", actas_cap, "vs", value_counts4)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('4.- Validación de Actas Capturadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_capturadas_coinciden():
    """
    Prueba que los valores de ACTAS_CAPTURADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_CAPTURADAS con los esperados"):
        if np.array_equal(value_counts4, actas_cap):
            allure.attach(
                f"4.- Los valores de ACTAS_CAPTURADAS coinciden: {actas_cap}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"4.- Los valores de ACTAS_CAPTURADAS no coinciden. {actas_cap} vs {value_counts4}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts4, actas_cap), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts5, actas_cap_por):
    print("[green]5.- Los valores de PORCENTAJE_ACTAS_CAPTURADAS coinciden:[/green]",actas_cap_por)
else:
    print("[red]5.- Los valores de PORCENTAJE_ACTAS_CAPTURADAS no coinciden.[/red]", actas_cap_por, "vs", value_counts5)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('5.- Validación de Porcentaje de Actas Capturadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_capturadas_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_CAPTURADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_CAPTURADAS con los esperados"):
        if np.array_equal(value_counts5, actas_cap_por):
            allure.attach(
                f"5.- Los valores de PORCENTAJE_ACTAS_CAPTURADAS coinciden: {actas_cap_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"5.- Los valores de PORCENTAJE_ACTAS_CAPTURADAS no coinciden. {actas_cap_por} vs {value_counts4}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts5, actas_cap_por), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts, actas_con):
    print("[green]6.- Los valores de ACTAS_CONTABILIZADAS coinciden:[/green]", actas_con)
else:
    print("[red]6.- Los valores de ACTAS_CONTABILIZADAS no coinciden.[/red]", actas_con)
    print(value_counts)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('6.- Validación de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_contabilizadas_coinciden():
    """
    Prueba que los valores de ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts, actas_con):
            allure.attach(
                f"6.- Los valores de ACTAS_CONTABILIZADAS coinciden: {actas_con}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"6.- Los valores de ACTAS_CONTABILIZADAS no coinciden. {actas_con} vs {value_counts}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts, actas_con), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts6, actas_con_por):
    print("[green]7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coinciden:[/green]", actas_con_por)
else:
    print("[red]7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS no coinciden.[/red]", actas_con_por)
    print(value_counts6)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('7.- Validación de Porcentaje de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_contabilizadas_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts6, actas_con_por):
            allure.attach(
                f"7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coinciden: {actas_con_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS no coinciden. {actas_con_por} vs {value_counts6}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts6, actas_con_por), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts7, actas_incon_por):
    print("[green]8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coinciden:[/green]", actas_incon_por)
else:
    print("[red]8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS no coinciden.[/red]", actas_incon_por, "vs", value_counts7)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('8.- Validación de Porcentaje de Actas con Inconcistencias')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_inconsistencias_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS con los esperados"):
        if np.array_equal(value_counts7, actas_incon_por):
            allure.attach(
                f"8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coinciden: {actas_incon_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS no coinciden. {actas_incon_por} vs {value_counts7}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts7, actas_incon_por), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts2, actas_nocon):
    print("[green]9.- Los valores de ACTAS_NO_CONTABILIZADAS coinciden:[/green]", actas_nocon)
else:
    print("[red]9.- Los valores de ACTAS_NO_CONTABILIZADAS no coinciden.[/red]", actas_nocon)
    print(value_counts2)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('9.- Validación de Actas No Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_no_contabilizadas_coinciden():
    """
    Prueba que los valores de ACTAS_NO_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_NO_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts2, actas_nocon):
            allure.attach(
                f"9.- Los valores de ACTAS_NO_CONTABILIZADAS coinciden: {actas_nocon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"9.- Los valores de ACTAS_NO_CONTABILIZADAS no coinciden. {actas_nocon} vs {value_counts2}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts2, actas_nocon), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts8, lnactascon):
    print("[green]10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coinciden:[/green]", lnactascon)
else:
    print("[red]10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS no coinciden.[/red]", lnactascon)
    print(value_counts8)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('10.- Validación de Lista Nominal de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_lista_nominal_actas_contabilizadas_coinciden():
    """
    Prueba que los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts8, lnactascon):
            allure.attach(
                f"10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coinciden: {lnactascon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS no coinciden. {lnactascon} vs {value_counts8}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts8, lnactascon), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts10, totalvotosc):
    print("[green]11.- Los valores de TOTAL_VOTOS_C_CS coinciden:[/green]", totalvotosc)
else:
    print("[red]11.- Los valores de TOTAL_VOTOS_C_CS no coinciden.[/red]", totalvotosc)
    print(value_counts10)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('11.- Validación de Total Votos C_CS')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_total_votos_c_cs_coinciden():
    """
    Prueba que los valores de TOTAL_VOTOS_C_CS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de TOTAL_VOTOS_C_CS con los esperados"):
        if np.array_equal(value_counts10, totalvotosc):
            allure.attach(
                f"11.- Los valores de TOTAL_VOTOS_C_CS coinciden: {totalvotosc}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"11.- Los valores de TOTAL_VOTOS_C_CS no coinciden. {totalvotosc} vs {value_counts10}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts10, totalvotosc), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts11, totalvotoss):
    print("[green]12.- Los valores de TOTAL_VOTOS_S_CS coinciden:[/green]", totalvotoss)
else:
    print("[red]12.- Los valores de TOTAL_VOTOS_S_CS no coinciden.[/red]", totalvotoss)
    print(value_counts11)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('12.- Validación de Total de Votos S_CS')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_total_votos_s_cs_coinciden():
    """
    Prueba que los valores de TOTAL_VOTOS_S_CS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de TOTAL_VOTOS_S_CS con los esperados"):
        if np.array_equal(value_counts11, totalvotoss):
            allure.attach(
                f"12.- Los valores de TOTAL_VOTOS_S_CS coinciden: {totalvotoss}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"12.- Los valores de TOTAL_VOTOS_S_CS no coinciden. {totalvotoss} vs {value_counts11}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts11, totalvotoss), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )

if np.array_equal(value_counts9, participacionciu):
    print("[green]13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coinciden:[/green]", participacionciu)
else:
    print("[red]13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA no coinciden.[/red]", participacionciu)
    print(value_counts9)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('13.- Validación de Porcentaje de Participación Ciudadana')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_porcentaje_participacion_ciudadana_coinciden():
    """
    Prueba que los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_PARTICIPACION_CIUDADANA con los esperados"):
        if np.array_equal(value_counts9, participacionciu):
            allure.attach(
                f"13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coinciden: {participacionciu}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA no coinciden. {participacionciu} vs {value_counts9}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        assert np.array_equal(value_counts9, participacionciu), (
            "Los valores no coinciden. Revisa el reporte para más detalles."
        )