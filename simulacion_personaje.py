import random
import uuid
from datetime import timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# ==============================================================================
# 1. SEMILLAS DE REPRODUCIBILIDAD
# ==============================================================================
# Garantizan que cada ejecucion genere exactamente los mismos datos
random.seed(42)
Faker.seed(42)

# ==============================================================================
# 2. DEFINICION DE CONSTANTES Y LISTAS DE DOMINIO (TABLA: personaje)
# ==============================================================================
FILAS = 400
FALSITO = Faker("es_CO")

CLASIFICACIONES = [
    "TODO_PUBLICO",
    "MAYORES_13",
    "MAYORES_18",
    "NSFW"
]

ESTADOS_MODERACION = [
    "aprobado",
    "pendiente",
    "rechazado",
    "en_revision"
]

MODOS_ANIMACION = [
    "estatico",
    "animado",
    "bucle_portadas"
]

GENEROS = [
    "Masculino",
    "Femenino",
    "No binario",
    "Androide",
    "Desconocido"
]

POOL_TAGS = [
  'Tsundere',
  'Yandere',
  'Dominante',
  'Sumiso',
  'Protector',
  'Tímido',
  'Seductor',
  'Misterioso',
  'Rebelde',
  'Frío / Distante',
  'Dulce / Tierno',
  'Enemigos a amantes',
  'Mejores amigos',
  'Amor prohibido',
  'Romance lento',
  'Matrimonio arreglado',
  'Jefe y empleado',
  'Compañero de cuarto',
  'Amor no correspondido',
  'Extraños a amantes',
  'Vampiro',
  'Hombre lobo',
  'Demonio',
  'Ángel',
  'Realeza / Príncipe',
  'Mafia / Yakuza',
  'Hechicero / Brujo',
  'Detective',
  'Militar / Soldado',
  'Celebridad / Idol',
  'Monstruo / Híbrido',
  'Villano',
  'Héroe',
  'Romance',
  'Picante (+18)',
  'Drama',
  'Comedia / Divertido',
  'Fantasía Medieval',
  'Cyberpunk / Sci-Fi',
  'Sobrenatural / Terror',
  'Universidad',
  'Vida cotidiana',
  'Apocalipsis / Supervivencia'
]

MOTIVOS_ELIMINACION = [
    "Infraccion de normas comunitarias",
    "Solicitud del creador",
    "Contenido duplicado o spam",
    "Violacion de derechos de autor"
]


# ==============================================================================
# 3. FUNCION GENERADORA DE DATOS LIMPIOS
# ==============================================================================
def generar_datos_personajes(numero_filas=FILAS):
    """
    Genera una lista de diccionarios representando los registros de la tabla 'personaje'
    respetando tipos de datos, restricciones y valores nulos/predeterminados.
    """
    personajes = []
    
    for i in range(1, numero_filas + 1):
        # 1. id_personaje (INT AUTO_INCREMENT)
        id_personaje = i
        
        # 2. cid (VARCHAR(20) - Identificador unico de personaje, ej: CID-A8F2913C)
        cid = f"CID-{uuid.uuid4().hex[:12].upper()}"
        
        # 3. id_categoria (INT NULL) - Llave foranea a categoria (1 a 10, o None 10% de las veces)
        id_categoria = random.choice([None] + list(range(1, 11)))
        
        # 4. id_creador (INT NULL) - Llave foranea a usuario creador (1 a 50, o None 5% de las veces)
        id_creador = random.choice([None] + list(range(1, 51)))
        
        # 5. nombre (VARCHAR(100) NOT NULL)
        nombre = f"{FALSITO.first_name()} {FALSITO.last_name()}"
        
        # 6. descripcion_corta (TEXT NULL)
        descripcion_corta = FALSITO.sentence(nb_words=10) if random.random() > 0.10 else None
        
        # 7. avatar_url (VARCHAR(255) NULL)
        avatar_url = f"https://api.holo-ai.com/avatars/{cid.lower()}.png" if random.random() > 0.05 else None
        
        # 8. publico (TINYINT(1) DEFAULT 1) - 1 o 0
        publico = 1 if random.random() > 0.20 else 0
        
        # 9. clasificacion_contenido (VARCHAR(255) NOT NULL)
        clasificacion_contenido = random.choice(CLASIFICACIONES)
        
        # 10. estado_moderacion (VARCHAR(255) NOT NULL)
        estado_moderacion = random.choice(ESTADOS_MODERACION)
        
        # 11. fecha_creacion (DATETIME NULL DEFAULT current_timestamp())
        fecha_creacion = FALSITO.date_time_between(start_date="-2y", end_date="now")
        
        # 12. es_oficial (BIT(1) NOT NULL) - 1 (oficial de la plataforma) o 0 (creado por usuario)
        es_oficial = 1 if random.random() < 0.15 else 0
        
        # 13. genero (VARCHAR(30) NULL)
        genero = random.choice(GENEROS) if random.random() > 0.10 else None
        
        # 14. tags (TEXT NULL) - Lista separada por comas
        tags_seleccionados = random.sample(POOL_TAGS, k=random.randint(1, 4))
        tags = ", ".join(tags_seleccionados) if random.random() > 0.10 else None
        
        # 15. fecha_eliminacion & 16. motivo_eliminacion (DATETIME & VARCHAR(255) NULL)
        # Solo el 12% estan eliminados (Soft Delete)
        if random.random() < 0.12:
            # La fecha de eliminacion debe ser posterior a la fecha de creacion
            dias_despues = random.randint(1, 60)
            fecha_eliminacion = fecha_creacion + timedelta(days=dias_despues)
            motivo_eliminacion = random.choice(MOTIVOS_ELIMINACION)
        else:
            fecha_eliminacion = None
            motivo_eliminacion = None
            
        # 17. modo_animacion_portada (VARCHAR(30) DEFAULT 'estatico')
        modo_animacion_portada = random.choice(MODOS_ANIMACION)
        
        # 18. avatar_animado_url (VARCHAR(500) NULL)
        # Si tiene animacion o bucle, suele tener URL de WebP o GIF
        if modo_animacion_portada in ["animado", "bucle_portadas"] and random.random() > 0.15:
            formato = random.choice(["webp", "gif"])
            avatar_animado_url = f"https://api.holo-ai.com/animados/{cid.lower()}.{formato}"
        else:
            avatar_animado_url = None

        personajes.append({
            "id_personaje": id_personaje,
            "cid": cid,
            "id_categoria": id_categoria,
            "id_creador": id_creador,
            "nombre": nombre,
            "descripcion_corta": descripcion_corta,
            "avatar_url": avatar_url,
            "publico": publico,
            "clasificacion_contenido": clasificacion_contenido,
            "estado_moderacion": estado_moderacion,
            "fecha_creacion": fecha_creacion,
            "es_oficial": es_oficial,
            "genero": genero,
            "tags": tags,
            "fecha_eliminacion": fecha_eliminacion,
            "motivo_eliminacion": motivo_eliminacion,
            "modo_animacion_portada": modo_animacion_portada,
            "avatar_animado_url": avatar_animado_url
        })
        
    return personajes


# ==============================================================================
# 4. FUNCIONES AUXILIARES PARA INTRODUCIR ERRORES / SUCIO (DATA DIRTYING)
# ==============================================================================
def obtener_muestra(datos_df, porcentaje):
    """Retorna los indices de una muestra aleatoria segun el porcentaje dado."""
    return datos_df.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

def escribir_con_errores(texto):
    """Aplica variaciones tipograficas: mayusculas, espacios, o cambios."""
    if not isinstance(texto, str):
        return texto
    variantes = [
        texto.lower(),
        texto.upper(),
        texto.capitalize(),
        f"  {texto}  ",
        texto.replace("a", "4").replace("e", "3")
    ]
    return random.choice(variantes)

def convertir_booleano_sucio(valor):
    """Convierte booleanos/bits a representaciones inconsistentes de texto."""
    if valor in [1, True, "1"]:
        return random.choice(["SI", "true", "True", "1", "S", 1])
    else:
        return random.choice(["NO", "false", "False", "0", "N", 0])


# ==============================================================================
# 5. FUNCION PRINCIPAL DE ENSUCIADO DE DATOS
# ==============================================================================
def ensuciar_personajes(datos_df):
    """
    Introduce de forma intencional ruido y datos sucios comunes en la vida real:
    - Espacios y cambios de mayusculas/minusculas en nombres y estados
    - URLs rotas o sin protocolo http/https
    - Nulos inesperados en campos obligatorios
    - Fechas con formatos mixtos (ISO vs Latinoamericano)
    - Booleanos representados como texto ('SI', 'NO', '1', '0')
    - Formatos de tags desordenados (puntos y comas, espacios irregulares)
    """
    datos_df = datos_df.copy()

    # 1. Nombre: 10% con espacios extra y 8% en MAYUSCULAS
    filas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas, "nombre"] = "   " + datos_df.loc[filas, "nombre"] + " "
    
    filas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas, "nombre"] = datos_df.loc[filas, "nombre"].str.upper()

    # 2. CID: 5% en minusculas y 3% con espacios
    filas = obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas, "cid"] = datos_df.loc[filas, "cid"].str.lower()

    # 3. Avatar URL: 6% de URLs danadas (sin 'https://') y 4% nulos no deseados
    filas = obtener_muestra(datos_df, 0.06)
    datos_df.loc[filas, "avatar_url"] = datos_df.loc[filas, "avatar_url"].astype(str).str.replace("https://", "htp://")
    
    filas = obtener_muestra(datos_df, 0.04)
    datos_df.loc[filas, "avatar_url"] = None

    # 4. Clasificacion de contenido y Estado de moderacion: errores de escritura
    filas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas, "estado_moderacion"] = datos_df.loc[filas, "estado_moderacion"].map(escribir_con_errores)

    filas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas, "modo_animacion_portada"] = datos_df.loc[filas, "modo_animacion_portada"].map(escribir_con_errores)

    # 5. Booleanos (publico y es_oficial): valores mezclados ('SI', 'NO', 1, 0, 'True')
    datos_df["publico"] = datos_df["publico"].astype(object)
    filas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas, "publico"] = datos_df.loc[filas, "publico"].map(convertir_booleano_sucio)

    datos_df["es_oficial"] = datos_df["es_oficial"].astype(object)
    filas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas, "es_oficial"] = datos_df.loc[filas, "es_oficial"].map(convertir_booleano_sucio)

    # 6. Tags: mezclar separadores (cambiar comas por ';' o '/') en el 12%
    filas = obtener_muestra(datos_df, 0.12)
    datos_df.loc[filas, "tags"] = datos_df.loc[filas, "tags"].astype(str).str.replace(", ", ";")

    # 7. Fechas: Mezcla de formato ISO (YYYY-MM-DD HH:MM:SS) y Latino (DD/MM/YYYY HH:MM)
    fechas_validas = datos_df["fecha_creacion"].dropna()
    iso = fechas_validas.dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = fechas_validas.dt.strftime("%d/%m/%Y %H:%M")
    
    datos_df["fecha_creacion"] = iso
    filas = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas, "fecha_creacion"] = latino.loc[filas]

    # Mismo formato mixto para fecha_eliminacion (donde no sea nulo)
    filas_con_eliminacion = datos_df[datos_df["fecha_eliminacion"].notna()].index
    if len(filas_con_eliminacion) > 0:
        fechas_elim = datos_df.loc[filas_con_eliminacion, "fecha_eliminacion"]
        iso_elim = fechas_elim.dt.strftime("%Y-%m-%d %H:%M:%S")
        lat_elim = fechas_elim.dt.strftime("%d/%m/%Y %H:%M")
        datos_df.loc[filas_con_eliminacion, "fecha_eliminacion"] = iso_elim
        
        # 30% de las fechas eliminadas en formato latino
        muestra_elim = datos_df.loc[filas_con_eliminacion].sample(frac=0.30, random_state=42).index
        datos_df.loc[muestra_elim, "fecha_eliminacion"] = lat_elim.loc[muestra_elim]

    return datos_df


# ==============================================================================
# 6. BLOQUE DE EJECUCION Y PRUEBA
# ==============================================================================
if __name__ == "__main__":
    print("==================================================================")
    print("   GENERANDO SIMULACION DE DATOS: TABLA 'personaje'               ")
    print("==================================================================")
    
    # 1. Generar datos limpios en un DataFrame de Pandas
    datos_limpios = generar_datos_personajes(FILAS)
    df_personajes_limpio = pd.DataFrame(datos_limpios)
    
    print(f"\n[+] Generadas {len(df_personajes_limpio)} filas de personajes limpios.")
    print("\n--- Vista previa de datos limpios (primeras 5 filas) ---")
    print(df_personajes_limpio[["id_personaje", "cid", "nombre", "clasificacion_contenido", "estado_moderacion", "publico"]].head())

    # 2. Aplicar proceso de ensuciado
    df_personajes_sucio = ensuciar_personajes(df_personajes_limpio)
    
    print("\n--- Vista previa de datos ensuciados (primeras 5 filas) ---")
    print(df_personajes_sucio[["id_personaje", "cid", "nombre", "estado_moderacion", "publico", "tags", "fecha_creacion"]].head())

    # 3. Exportar opcionalmente a Excel y CSV
    ruta_excel = Path(__file__).with_name("personajes_sucios.xlsx")
    ruta_csv = Path(__file__).with_name("personajes_sucios.csv")
    
    df_personajes_sucio.to_excel(ruta_excel, index=False, sheet_name="personajes")
    df_personajes_sucio.to_csv(ruta_csv, index=False, encoding="utf-8")
    
    print(f"\n[OK] Archivos generados exitosamente:")
    print(f"     - Excel: {ruta_excel.name}")
    print(f"     - CSV:   {ruta_csv.name}")
    print("==================================================================")
