import random
import pandas as pd
from faker import Faker

# ==============================================================================
# Semillas fijas para garantizar reproducibilidad
# ==============================================================================
random.seed(42)
Faker.seed(42)

fake = Faker("es_CO")

# ==============================================================================
# Constantes del dominio
# ==============================================================================
CLASIFICACIONES = ['SFW', 'NSFW', 'PG-13', 'Todo Publico']
ESTADOS_MODERACION = ['aprobado', 'pendiente', 'rechazado']


def generar_personajes(n=300):
    """
    Genera un DataFrame con n registros simulados de la tabla 'personajes'
    y aplica ensuciamiento intencional segun los criterios de aceptacion.
    """
    datos = []
    
    # --------------------------------------------------------------------------
    # 1. Generacion Base
    # --------------------------------------------------------------------------
    for i in range(1, n + 1):
        datos.append({
            "id_personaje": i,
            "id_categoria": random.randint(1, 10),
            "id_creador": random.randint(1, 100),
            "nombre": fake.first_name() + " " + fake.word().capitalize(),
            "descripcion_corta": fake.sentence(nb_words=10),
            "avatar_url": fake.image_url(),
            "publico": random.choice([0, 1]),
            "clasificacion_contenido": random.choice(CLASIFICACIONES),
            "estado_moderacion": random.choice(ESTADOS_MODERACION),
            "fecha_creacion": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "es_oficial": random.choices([0, 1], weights=[0.85, 0.15])[0]
        })
        
    df = pd.DataFrame(datos)

    # --------------------------------------------------------------------------
    # 2. Reglas de Ensuciamiento Intencional
    # --------------------------------------------------------------------------
    
    # nombre: 12% con espacios sobrantes al inicio y final
    idx = df.sample(frac=0.12, random_state=random.randint(0, 10000)).index
    df.loc[idx, "nombre"] = "   " + df.loc[idx, "nombre"] + " "

    # nombre: 8% en minusculas totales o MAYUSCULAS sostenidas
    idx = df.sample(frac=0.08, random_state=random.randint(0, 10000)).index
    df.loc[idx, "nombre"] = df.loc[idx, "nombre"].apply(
        lambda x: x.lower() if random.random() < 0.5 else x.upper()
    )

    # nombre: caracteres extranos ocasionales ("???", "--")
    idx = df.sample(frac=0.04, random_state=random.randint(0, 10000)).index
    df.loc[idx, "nombre"] = df.loc[idx, "nombre"].apply(
        lambda x: random.choice([f"???{x}", f"{x}???", f"--{x}--", "???"])
    )

    # descripcion_corta: 10% en None (nulos)
    idx = df.sample(frac=0.10, random_state=random.randint(0, 10000)).index
    df.loc[idx, "descripcion_corta"] = None

    # descripcion_corta: 5% como cadenas vacias ("") o solo espacios ("   ")
    no_nulos = df[df["descripcion_corta"].notna()].index
    idx = df.loc[no_nulos].sample(frac=0.05, random_state=random.randint(0, 10000)).index
    df.loc[idx, "descripcion_corta"] = [random.choice(["", "   "]) for _ in range(len(idx))]

    # avatar_url: 8% en None
    idx = df.sample(frac=0.08, random_state=random.randint(0, 10000)).index
    df.loc[idx, "avatar_url"] = None

    # avatar_url: 5% con URLs rotas o sin protocolo (ej. www.ejemplo sin http o ht tp://url rota)
    no_nulos = df[df["avatar_url"].notna()].index
    idx = df.loc[no_nulos].sample(frac=0.05, random_state=random.randint(0, 10000)).index
    def romper_url(url):
        variantes = [
            url.replace("https://", "www.").replace("http://", "www."),
            url.replace("https://", "ht tp://").replace("http://", "ht tp://"),
            "www.ejemplo",
            "htp://url rota"
        ]
        return random.choice(variantes)
    df.loc[idx, "avatar_url"] = df.loc[idx, "avatar_url"].apply(romper_url)

    # id_categoria: 5% en None
    df["id_categoria"] = df["id_categoria"].astype(object)
    idx = df.sample(frac=0.05, random_state=random.randint(0, 10000)).index
    df.loc[idx, "id_categoria"] = None

    # id_categoria: 3% con IDs inexistentes o negativos (-1, 999)
    idx = df.sample(frac=0.03, random_state=random.randint(0, 10000)).index
    df.loc[idx, "id_categoria"] = [random.choice([-1, 999]) for _ in range(len(idx))]

    # id_creador: 7% en None (especialmente para personajes oficiales o huerfanos)
    df["id_creador"] = df["id_creador"].astype(object)
    idx = df.sample(frac=0.07, random_state=random.randint(0, 10000)).index
    df.loc[idx, "id_creador"] = None

    # publico y es_oficial: Mezcla de formatos booleanos: True, False, '1', '0', 'true', 'SI', 'NO'
    df["publico"] = df["publico"].astype(object)
    df["es_oficial"] = df["es_oficial"].astype(object)

    def mezclar_booleano(val):
        if val in [1, True, '1', 'true', 'True', 'SI']:
            return random.choice([True, '1', 'true', 'SI', 1])
        else:
            return random.choice([False, '0', 'false', 'NO', 0])

    idx_pub = df.sample(frac=0.25, random_state=random.randint(0, 10000)).index
    df.loc[idx_pub, "publico"] = df.loc[idx_pub, "publico"].apply(mezclar_booleano)

    idx_ofi = df.sample(frac=0.25, random_state=random.randint(0, 10000)).index
    df.loc[idx_ofi, "es_oficial"] = df.loc[idx_ofi, "es_oficial"].apply(mezclar_booleano)

    # clasificacion_contenido: Inconsistencias de formato: 'sfw', 'SFW ', 'pg13', 'TODO PUBLICO'
    idx = df.sample(frac=0.15, random_state=random.randint(0, 10000)).index
    mapa_clasificacion = {
        'SFW': ['sfw', 'SFW '],
        'NSFW': ['nsfw', ' NSFW'],
        'PG-13': ['pg13', 'pg-13', 'PG13'],
        'Todo Publico': ['TODO PUBLICO', 'todo publico', 'Todo publico ']
    }
    df.loc[idx, "clasificacion_contenido"] = df.loc[idx, "clasificacion_contenido"].apply(
        lambda x: random.choice(mapa_clasificacion.get(x, ['TODO PUBLICO', 'sfw']))
    )

    # estado_moderacion: Inconsistencias: 'APROBADO', ' pendiente', 'rechazado'
    idx = df.sample(frac=0.15, random_state=random.randint(0, 10000)).index
    mapa_moderacion = {
        'aprobado': ['APROBADO', ' Aprobado', 'aprobado '],
        'pendiente': [' pendiente', 'PENDIENTE', 'pendiente '],
        'rechazado': ['RECHAZADO', ' rechazado', 'Rechazado ']
    }
    df.loc[idx, "estado_moderacion"] = df.loc[idx, "estado_moderacion"].apply(
        lambda x: random.choice(mapa_moderacion.get(x, ['APROBADO', ' pendiente']))
    )

    # Nombres repetidos: 4% de nombres duplicados para distintos personajes
    idx_dest = df.sample(frac=0.04, random_state=random.randint(0, 10000)).index
    idx_fuente = df.drop(idx_dest).sample(n=len(idx_dest), random_state=random.randint(0, 10000)).index
    df.loc[idx_dest, "nombre"] = df.loc[idx_fuente, "nombre"].values

    # Duplicados: 5% de las filas repetidas tal cual (duplicados exactos)
    num_duplicados = int(len(df) * 0.05)
    filas_duplicadas = df.sample(n=num_duplicados, random_state=random.randint(0, 10000))
    df = pd.concat([df, filas_duplicadas], ignore_index=True)

    return df


if __name__ == "__main__":
    df = generar_personajes(300)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
