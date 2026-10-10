import random
import pandas as pd
from faker import Faker

# =============================================================================
# 1. SEMILLAS DE REPRODUCIBILIDAD
# =============================================================================
Faker.seed(42)
random.seed(42)

fake = Faker("es_CO")

# =============================================================================
# 2. CONSTANTES GLOBALES
# =============================================================================
GENEROS = ['masculino', 'femenino', 'otro']
PROVEEDORES_AUTH = ['local', 'google', 'apple', 'github']
ESTADOS = ['activo', 'suspendido', 'baneado']
ROLES = ['usuario', 'admin']


# =============================================================================
# 3. FUNCIÓN GENERADORA Y ENSUCIADORA
# =============================================================================
def generar_usuarios(n=300):
    """
    Genera n registros base para la tabla 'usuarios' con las columnas de Backend II
    y aplica reglas de ensuciamiento intencional.
    Devuelve un DataFrame de pandas.
    """
    # -------------------------------------------------------------------------
    # Generación Base (n filas)
    # -------------------------------------------------------------------------
    usuarios = []
    
    for i in range(1, n + 1):
        proveedor = random.choice(PROVEEDORES_AUTH)
        
        # contrasena_hash: fake.sha256() si proveedor_auth == 'local', de lo contrario None
        if proveedor == 'local':
            contrasena_hash = fake.sha256()
        else:
            contrasena_hash = None

        # id_plan: peso mayor al plan 1
        id_plan = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]

        # fecha_nacimiento entre 13 y 70 años
        fecha_nac = fake.date_of_birth(minimum_age=13, maximum_age=70).strftime("%Y-%m-%d")

        # estado con probabilidades específicas
        estado = random.choices(ESTADOS, weights=[0.8, 0.15, 0.05])[0]

        # fecha_registro en los últimos 2 años
        fecha_reg = fake.date_time_between(start_date="-2y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")

        # rol: 90% usuario, 10% admin
        rol = random.choices(ROLES, weights=[0.9, 0.1])[0]

        registro = {
            "id_usuario": i,
            "nombre_usuario": fake.user_name(),
            "correo": fake.email(),
            "genero": random.choice(GENEROS),
            "contrasena_hash": contrasena_hash,
            "proveedor_auth": proveedor,
            "id_plan": id_plan,
            "fecha_nacimiento": fecha_nac,
            "edad_verificada": random.choice([0, 1]),
            "gemas_saldo": random.randint(0, 500),
            "estado": estado,
            "fecha_registro": fecha_reg,
            "rol": rol
        }
        usuarios.append(registro)

    df = pd.DataFrame(usuarios)

    # -------------------------------------------------------------------------
    # Reglas de Ensuciamiento Intencional
    # -------------------------------------------------------------------------

    # 1. nombre_usuario: 10% espacios sobrantes inicio/final; 10% en MAYÚSCULAS
    idx_espacios = df.sample(frac=0.10, random_state=42).index
    df.loc[idx_espacios, "nombre_usuario"] = "  " + df.loc[idx_espacios, "nombre_usuario"] + " "

    idx_mayus = df.sample(frac=0.10, random_state=99).index
    df.loc[idx_mayus, "nombre_usuario"] = df.loc[idx_mayus, "nombre_usuario"].str.upper()

    # 2. correo:
    # - 6% sin arroba o sin dominio (ej. usuario.dominio.com)
    idx_sin_arroba = df.sample(frac=0.06, random_state=12).index
    df.loc[idx_sin_arroba, "correo"] = df.loc[idx_sin_arroba, "correo"].str.replace("@", ".")

    # - 4% mayúsculas mezcladas
    idx_mayus_correo = df.sample(frac=0.04, random_state=34).index
    df.loc[idx_mayus_correo, "correo"] = df.loc[idx_mayus_correo, "correo"].str.swapcase()

    # - 3% correos duplicados entre distintos usuarios (debería ser único)
    idx_dup_correo = df.sample(frac=0.03, random_state=56).index
    correo_referencia = df.loc[0, "correo"]
    df.loc[idx_dup_correo, "correo"] = correo_referencia

    # 3. genero:
    # - Variantes con inconsistencias de formato: 'MASCULINO', 'femenino ', 'Otro', 'M', 'F'
    variantes_genero = ['MASCULINO', 'femenino ', 'Otro', 'M', 'F']
    idx_inconsistencias_genero = df.sample(frac=0.15, random_state=78).index
    df.loc[idx_inconsistencias_genero, "genero"] = [random.choice(variantes_genero) for _ in idx_inconsistencias_genero]

    # - 8% en None
    idx_genero_none = df.sample(frac=0.08, random_state=90).index
    df.loc[idx_genero_none, "genero"] = None

    # 4. proveedor_auth: Variantes con mayúsculas y espacios ('GOOGLE', ' local ', 'Apple')
    variantes_auth = {
        'google': 'GOOGLE',
        'local': ' local ',
        'apple': 'Apple',
        'github': 'GitHub '
    }
    idx_auth = df.sample(frac=0.15, random_state=101).index
    df.loc[idx_auth, "proveedor_auth"] = df.loc[idx_auth, "proveedor_auth"].map(lambda x: variantes_auth.get(x, x))

    # 5. fecha_nacimiento:
    # - Mezcla de formatos: 'YYYY-MM-DD' vs 'DD/MM/YYYY'
    idx_formato_fecha = df.sample(frac=0.20, random_state=112).index
    fechas_convertidas = pd.to_datetime(df.loc[idx_formato_fecha, "fecha_nacimiento"]).dt.strftime("%d/%m/%Y")
    df.loc[idx_formato_fecha, "fecha_nacimiento"] = fechas_convertidas

    # - 5% con valores ilógicos (fechas futuras o años como 1902)
    fechas_ilogicas = ['2050-01-01', '1902-05-14', '2099-12-31', '1899-10-10']
    idx_fechas_raras = df.sample(frac=0.05, random_state=123).index
    df.loc[idx_fechas_raras, "fecha_nacimiento"] = [random.choice(fechas_ilogicas) for _ in idx_fechas_raras]

    # 6. edad_verificada: A veces texto o booleano ('SI', 'NO', True, False, '1', '0')
    df["edad_verificada"] = df["edad_verificada"].astype(object)
    variantes_bool = ['SI', 'NO', True, False, '1', '0']
    idx_edad_verificada = df.sample(frac=0.20, random_state=134).index
    df.loc[idx_edad_verificada, "edad_verificada"] = [random.choice(variantes_bool) for _ in idx_edad_verificada]

    # 7. gemas_saldo:
    df["gemas_saldo"] = df["gemas_saldo"].astype(object)
    # - 4% con valores negativos (ej. -50)
    idx_gemas_negativas = df.sample(frac=0.04, random_state=145).index
    df.loc[idx_gemas_negativas, "gemas_saldo"] = -1 * random.randint(10, 100)

    # - 3% como texto (ej. '100 gems')
    idx_gemas_texto = df.sample(frac=0.03, random_state=156).index
    df.loc[idx_gemas_texto, "gemas_saldo"] = [f"{random.randint(50, 300)} gems" for _ in idx_gemas_texto]

    # 8. estado: Inconsistencias de texto: 'ACTIVO', 'Activo ', 'baneado'
    variantes_estado = ['ACTIVO', 'Activo ', 'baneado ']
    idx_estado = df.sample(frac=0.15, random_state=167).index
    df.loc[idx_estado, "estado"] = [random.choice(variantes_estado) for _ in idx_estado]

    # 9. Duplicados: 5% de las filas repetidas tal cual (duplicados exactos completos)
    filas_duplicadas = df.sample(frac=0.05, random_state=42)
    df = pd.concat([df, filas_duplicadas], ignore_index=True)

    return df


# =============================================================================
# 4. INSPECCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    df = generar_usuarios(300)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
