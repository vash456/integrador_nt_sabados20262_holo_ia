import random
import uuid 
from pathlib import Path

import pandas as pd
from faker import Faker 

#1 Sembrar semillas para los datos a simular 
random.seed(42)
Faker.seed(42)

#2 identificar los datos a simular con su tipo de usuario 
# id (texto (UUID)),
# nombre (texto),
# nit (texto), 
# sector (texto), 
# contacto (texto), 
# correo (texto), 
# telefono (texto), 
# activa (booleano)

#3 Establecer una constante para el número de simulaciones 
FILAS =400
ROLES=["administrador","empresario","estudiante","profesor"]
FALSITO=Faker("es_CO")


#4 Funcion generadora 
def generar_datos(numero_filas=400):
    usuarios=[]
    for _ in range(numero_filas):
        usuarios.append({
            "id":str(uuid.uuid4()),
            "name":FALSITO.name(),
            "correo":FALSITO.email(),
            "contrasena_hash":FALSITO.sha256(),
            "activo":random.choice([True,False]),
            "rol":random.choice(ROLES),
            "fecha_registro":FALSITO.date_time_between(start_date="-2y", end_date="now")
        })
    return usuarios

# generar tabla de excel con los datos simulados
# if __name__ == "__main__":
#     datos = generar_datos(FILAS)
#     archivo_excel = Path(__file__).with_name("usuarios.xlsx")
#     pd.DataFrame(datos).to_excel(archivo_excel, index=False, sheet_name="usuarios")
#     print(f"Datos guardados en: {archivo_excel}")

# 5. convirtiendo los datos generados en un dataframe con PANDAS
tabla_ordenada_usuarios = pd.DataFrame(generar_datos())

# 6. Probar la funcion
print(tabla_ordenada_usuarios.head(10))

# 7. preparar la simulacion para ensuciar mis datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes = [texto.lower(), texto.title(), texto.capitalize(),
                 f" {texto} ", "Juan Jose"]
    return random.choice(variantes)

# 7.3 Funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["NO", "0"])