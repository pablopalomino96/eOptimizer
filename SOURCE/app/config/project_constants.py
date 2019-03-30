#!/usr/bin/python3

import home_consumption as home

# Fichero de Constantes
# =====================
# Constantes respecto a EF (energia fotovoltaica)
# --------------------------------------------------
# Precio de cada modulo fotovoltaico (€)
MODULE_PRICE = 40
# Produccion anual estimada de un modulo (KW)
YEAR_PV_ESTIM = 96

# Constantes respecto a EB (energia de baterias)
# -------------------------------------------------
# Precio de la Baterías estacionaria (6 vasos, 12V) (€)
BAT_PRICE = 7500
# Profundidad de descarga
DISCH_DEPTH = 0.5
# Capacidad de Almacenaje en Kw
BAT_CAPACITY = 21

# Constantes respecto al Consumo
# ---------------------------------
# Consumo del sistema por funcionamiento (2KWh al dia) (KWh)
C_INT = 0.0888
# Consumo propio del hogar. Valor que debe ser satisfecho siempre
C = home.read_from_file()
# C = home.get_random_values()

# --------- API Aemet OpenData ---------
# Codigos de la API OpenData de AEMET
# Consuegra (Toledo)
# CITY_CODE = '45053'

# Api key para el manejo de OpenData AEMET
AEMET_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYWJsby5wYWxvbWlubzFAb3V0bG9vay5jb20iLCJqdGkiOiJmOGFhZTdiNi0yYWIzLTQzOTktYjU3Mi0zNDBlYWE2OGUwMDUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU0ODU4NTE1NywidXNlcklkIjoiZjhhYWU3YjYtMmFiMy00Mzk5LWI1NzItMzQwZWFhNjhlMDA1Iiwicm9sZSI6IiJ9.4VGEUO4v-ncytcyWuaNwHBBvhhIAW5r-5Es0VAFiLr8'

# url api AEMET OpenData
AEMET_URL = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/$CITY/?api_key={}'.format(AEMET_KEY)

# --------- API Esios REE ---------
# Token para la API de Esios (Red Electrica de España)
ESIOS_TOKEN = '879c5ab5bc0211a1ba23527736e3402a0e708f0a5e7c370f0274004e676ee5f6'

# Indicadores de precios Esios REE
PVPC = '1013' # Precio Voluntario para el Pequeño Consumidor (precio de compra de energia)
SPOT = '613'  # Precio marginal del intradiario (precio de venta a la red eletrica)

# url api Esios REE
ESIOS_URL = 'https://api.esios.ree.es/indicators/$INDICATOR?start_date=$START_DATE&end_date=$END_DATE'

# # Maxima Potencia Nominal posible (MNP) en W de un modulo fotovoltaico de Potencia Pico 50 W, de cada conjunto difuso del estado de Cielo
FUZZY_SETS = {
    'Despejado' : 48,
    'Poco nuboso' :43.16,
    'Nubes altas' : 38.16,
    'Intervalos nubosos' : 33.16,
    'Intervalos nubosos con lluvia escasa' : 28.16,
    'Intervalos nubosos con lluvia' : 23.16,
    'Nuboso' : 18.16,
    'Nuboso con lluvia escasa' : 13.16,
    'Cubierto' : 8.16,
    'Cubierto con lluvia escasa' : 2.66,
    'Nuboso noche' : 0,
    'Muy nuboso' : 0,
    'Nubes altas noche' : 0,
    'Intervalos nubosos con lluvia escasa noche' : 0,
    'Nuboso con lluvia escasa noche' : 0,
    'Muy nuboso con lluvia escasa' : 0,
    'Despejado noche' : 0,
    'Intervalos nubosos noche' : 0,
    'Poco nuboso noche' : 0,
    'Intervalos nubosos con lluvia noche' : 0,
    'Nuboso con lluvia' : 0,
    'Nuboso con lluvia noche' : 0,
    'Muy nuboso con lluvia' : 0,
    'Cubierto con lluvia' : 0,
    'Intervalos nubosos con nieve escasa' : 0,
    'Intervalos nubosos con nieve escasa noche' : 0,
    'Nuboso con nieve escasa' : 0,
    'Nuboso con nieve escasa noche' : 0,
    'Muy nuboso con nieve escasa' : 0,
    'Cubierto con nieve escasa' : 0,
    'Intervalos nubosos con nieve' : 0,
    'Intervalos nubosos con nieve noche' : 0,
    'Nuboso con nieve' : 0,
    'Nuboso con nieve noche' : 0,
    'Muy nuboso con nieve' : 0,
    'Cubierto con nieve' : 0,
    'Intervalos nubosos con tormenta' : 0,
    'Intervalos nubosos con tormenta noche' : 0,
    'Nuboso con tormenta' : 0,
    'Nuboso con tormenta noche' : 0,
    'Muy nuboso con tormenta' : 0,
    'Cubierto con tormenta' : 0,
    'Intervalos nubosos con tormenta y lluvia escasa' : 0,
    'Intervalos nubosos con tormenta y lluvia escasa noche' : 0,
    'Nuboso con tormenta y lluvia escasa' : 0,
    'Nuboso con tormenta y lluvia escasa noche' : 0,
    'Muy nuboso con tormenta y lluvia escasa' : 0,
    'Cubierto con tormenta y lluvia escasa' : 0
}
