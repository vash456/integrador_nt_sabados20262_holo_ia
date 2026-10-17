from pathlib import Path

# 1. Configuracion general de las rutas
NOMBRE_ENTIDAD = "personajes"
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos" / "crudos"
CARPETA_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "datos" / "reportes"

# 2. Funciones genericas para crear los archivos
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def exportar_csv(datos_df_sucios, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df_sucios.to_csv(ruta, sep=';')
    return ruta

def exportar_json(datos_df_sucios, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df_sucios.to_json(ruta, orient='records', incleardent="2")
    return ruta

def exportar_excel(datos_df_sucios, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df_sucios.to_excel(ruta, engine='openpyxl')
    return ruta

# 3. Llamamos las funciones para crear los archivos
def exportar_personajes(datos_df_sucios):
    return {
        "csv": exportar_csv(datos_df_sucios, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        "json": exportar_json(datos_df_sucios, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        "excel": exportar_excel(datos_df_sucios, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
    }
