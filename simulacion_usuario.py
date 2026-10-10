import numpy as np
import pandas as pd
import random
from faker import Faker


SEMILLA = 42
random.seed(SEMILLA)
np.random.seed(SEMILLA)
Faker.seed(SEMILLA)

fake = Faker("es_CO")

CANTIDAD_FILAS = 400

ROLES_VALIDOS = ["usuario", "admin"]
ESTADOS_VALIDOS = ["activo", "suspendido", "baneado"]
GENEROS_VALIDOS = ["masculino", "femenino", "otro"]
PROVEEDORES_AUTH = ["email", "google"]

def generar_usuarios_limpios(n=CANTIDAD_FILAS):
    
    registros = []
    
    for i in range(1, n + 1):
        # 80% de usuarios estándar, 20% admins
        rol = random.choices(ROLES_VALIDOS, weights=[0.85, 0.15])[0]
        # La gran mayoría activos
        estado = random.choices(ESTADOS_VALIDOS, weights=[0.80, 0.15, 0.05])[0]
        genero = random.choice(GENEROS_VALIDOS)
        proveedor = random.choices(PROVEEDORES_AUTH, weights=[0.7, 0.3])[0]
        
        fecha_nac = fake.date_of_birth(minimum_age=18, maximum_age=65)
        
        fecha_reg = fake.date_time_between(start_date="-2y", end_date="now")
        
        usuario = {
            "id_usuario": i,
            "nombre_usuario": fake.user_name(),
            "correo": fake.unique.email(),
            "genero": genero,
            "contrasena_hash": fake.sha256(),
            "proveedor_auth": proveedor,
            "id_plan": random.choice([1, 2, 3]),
            "fecha_nacimiento": fecha_nac.strftime("%Y-%m-%d"),
            "edad_verificada": 1 if random.random() > 0.3 else 0,
            "gemas_saldo": random.randint(0, 500),
            "estado": estado,
            "fecha_registro": fecha_reg,
            "rol": rol
        }
        registros.append(usuario)
        
    return pd.DataFrame(registros)


def obtener_muestra_indices(df, fraccion):
    """Obtiene una muestra aleatoria de índices del DataFrame según la fracción especificada."""
    return df.sample(frac=fraccion, random_state=random.randint(1, 10000)).index


def ensuciar_texto(texto):
    """Introduce errores de mayúsculas, minúsculas o valores 'NA'."""
    variantes = [
        texto.lower(),
        texto.upper(),
        texto.title(),
        f"  {texto}  ",
        "N/A",
        "NULL"
    ]
    return random.choice(variantes)


def ensuciar_booleano(valor):
    """Convierte 1/0 en representaciones inconsistentes (SI, NO, True, False, etc.)."""
    if valor == 1:
        return random.choice(["SI", "si", "True", "1", "verdadero"])
    else:
        return random.choice(["NO", "no", "False", "0", "falso"])


def ensuciar_datos(df_original):
    """
    Aplica errores e inconsistencias controladas a los datos limpios.
    Estos errores son los que posteriormente se resuelven en la fase de limpieza.
    """
    df = df_original.copy()

    # Error 1: Espacios en blanco innecesarios en 'nombre_usuario' (12% de filas)
    idx = obtener_muestra_indices(df, 0.12)
    df.loc[idx, "nombre_usuario"] = "  " + df.loc[idx, "nombre_usuario"] + " "

    # Error 2: Mayúsculas totales en 'nombre_usuario' (8% de filas)
    idx = obtener_muestra_indices(df, 0.08)
    df.loc[idx, "nombre_usuario"] = df.loc[idx, "nombre_usuario"].str.upper()

    # Error 3: Correos rotos sin '@' (5% de filas)
    idx = obtener_muestra_indices(df, 0.05)
    df.loc[idx, "correo"] = df.loc[idx, "correo"].str.replace("@", "")

    # Error 4: Correos nulos / faltantes (4% de filas)
    idx = obtener_muestra_indices(df, 0.04)
    df.loc[idx, "correo"] = None

    # Error 5: Géneros nulos (10% de filas)
    idx = obtener_muestra_indices(df, 0.10)
    df.loc[idx, "genero"] = None

    # Error 6: Inconsistencias tipográficas en 'rol' (10% de filas)
    idx = obtener_muestra_indices(df, 0.10)
    df.loc[idx, "rol"] = df.loc[idx, "rol"].map(ensuciar_texto)

    # Error 7: Inconsistencias en 'edad_verificada' (convertir 1/0 a texto mixto) (15% de filas)
    df["edad_verificada"] = df["edad_verificada"].astype(object)
    idx = obtener_muestra_indices(df, 0.15)
    df.loc[idx, "edad_verificada"] = df.loc[idx, "edad_verificada"].map(ensuciar_booleano)

    # Error 8: Formatos de fecha mixtos en 'fecha_registro'
    # Formato ISO (estándar DB): 'YYYY-MM-DD HH:MM:SS'
    # Formato Latino (inconsistente): 'DD/MM/YYYY HH:MM'
    iso = df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    df["fecha_registro"] = iso
    idx = obtener_muestra_indices(df, 0.25)
    df.loc[idx, "fecha_registro"] = latino.loc[idx]

    # Error 9: Saldo de gemas negativo (anomalía de negocio en 3% de filas)
    idx = obtener_muestra_indices(df, 0.03)
    df.loc[idx, "gemas_saldo"] = -1 * df.loc[idx, "gemas_saldo"]

    # Error 10: Filas duplicadas (inyección de registros repetidos)
    idx_duplicar = df.sample(n=10, random_state=42)
    df = pd.concat([df, idx_duplicar], ignore_index=True)

    return df



# =============================================================================
# 7. EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print(" PASO 1: Generando usuarios limpios con Faker...")
    print("=" * 60)
    df_limpio = generar_usuarios_limpios(CANTIDAD_FILAS)
    print(f"Total registros limpios generados: {len(df_limpio)}")
    print(df_limpio[["id_usuario", "nombre_usuario", "correo", "rol", "estado"]].head(5))

    print("\n" + "=" * 60)
    print(" PASO 2: Ensuciando datos a propósito...")
    print("=" * 60)
    df_sucio = ensuciar_datos(df_limpio)
    print(f"Total registros tras ensuciar (con duplicados): {len(df_sucio)}")
    print(df_sucio[["id_usuario", "nombre_usuario", "correo", "rol", "edad_verificada", "fecha_registro"]].head(8))

    print("\n" + "=" * 60)
    print(" PASO 3: Guardando en base de datos de simulación...")
    print("=" * 60)


    # También guardamos una copia en Excel para inspección visual
    archivo_excel = "usuarios_sucios.xlsx"
    try:
        df_sucio.to_excel(archivo_excel, index=False)
        print(f"[OK] Archivo Excel de inspección generado: {archivo_excel}")
    except PermissionError:
        print(f"[AVISO] No se pudo sobrescribir '{archivo_excel}' porque está abierto en Excel.")
        print("        (Ciérralo en Excel para actualizarlo en la próxima ejecución).")
    except Exception as e:
        print(f"[AVISO] No se pudo generar Excel: {e}")

    print("\n¡Simulación completada con éxito!")
