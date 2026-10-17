import random
import pandas as pd
from faker import Faker
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SEED (SEMILLA)
# ==========================================
# Al definir una semilla fija, los datos generados serán idénticos
# cada vez que ejecutes el script (reproducibilidad).
SEED = 42

random.seed(SEED)
Faker.seed(SEED)
fake = Faker("es_CO")  # Localización en español
fake.seed_instance(SEED)

# ==========================================
# 2. DEFINICIÓN DE REGLAS DE LA TABLA 'PAGOS'
# ==========================================
# enum('stripe', 'apple', 'google')
PROVEEDORES = ["stripe", "apple", "google"]

CONCEPTOS = [
    "Suscripción Mensual Pro",
    "Suscripción Anual VIP",
    "Paquete 500 Créditos IA",
    "Recarga 1000 Tokens de Conversación",
    "Desbloqueo de Personaje Holográfico",
    "Upgrade Plan Modelo Avanzado",
    "Pase Premium Trimestral"
]

MONTOS_COMUNES = [4.99, 9.99, 14.99, 19.99, 29.99, 49.99, 99.99]


def generar_id_externo(proveedor: str) -> str:
    """Genera un identificador realista según la pasarela usando Faker."""
    if proveedor == "stripe":
        return f"ch_{fake.hexify(text='^^^^^^^^^^^^^^^^^^^^^^^^')}"
    elif proveedor == "apple":
        return f"apl_{fake.random_number(digits=10, fix_len=True)}"
    elif proveedor == "google":
        return f"GPA.{fake.random_number(digits=4, fix_len=True)}-{fake.random_number(digits=4, fix_len=True)}-{fake.random_number(digits=4, fix_len=True)}-{fake.random_number(digits=5, fix_len=True)}"
    return fake.uuid4()


# ==========================================
# 3. GENERACIÓN DEL DATASET CON FAKER Y PANDAS
# ==========================================
def simular_dataset_pagos(cantidad: int = 100) -> pd.DataFrame:
    """
    Genera un DataFrame de Pandas con registros que cumplen con
    la estructura de la tabla 'pagos'.
    """
    registros = []
    
    for i in range(1, cantidad + 1):
        proveedor = fake.random_element(elements=PROVEEDORES)
        
        # 80% probabilidad de montos fijos típicos, 20% monto decimal libre
        if random.random() < 0.8:
            monto = fake.random_element(elements=MONTOS_COMUNES)
        else:
            monto = round(random.uniform(5.00, 150.00), 2)
            
        fecha_simulada = fake.date_time_between(start_date="-30d", end_date="now")

        registros.append({
            "id_pago": i,
            "id_usuario": fake.random_int(min=1, max=100),
            "monto": monto,
            "proveedor": proveedor,
            "id_externo": generar_id_externo(proveedor),
            "concepto": fake.random_element(elements=CONCEPTOS),
            "fecha_pago": fecha_simulada.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Crear el DataFrame de pandas
    df = pd.DataFrame(registros)
    
    # Asignar los tipos de datos adecuados
    df["monto"] = df["monto"].astype(float)
    df["fecha_pago"] = pd.to_datetime(df["fecha_pago"])
    
    return df


# ==========================================
# 4. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("=" * 65)
    print(f"  SIMULADOR DE TABLA 'PAGOS' CON FAKER Y PANDAS (SEED={SEED})  ")
    print("=" * 65)
    
    cant_str = input("¿Cuántos registros deseas generar? (por defecto 50): ").strip()
    cantidad = int(cant_str) if cant_str.isdigit() else 50
    
    # Generar DataFrame
    df_pagos = simular_dataset_pagos(cantidad)
    
    # Visualizar resumen de datos
    print("\n[+] Primeros 10 registros generados:")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    print(df_pagos.head(10))
    
    print("\n[+] Información del DataFrame:")
    print(df_pagos.info())
    
    # Exportar a CSV mediante Pandas
    nombre_csv = "pagos_simulados.csv"
    df_pagos.to_csv(nombre_csv, index=False, encoding="utf-8")
    print(f"\n[✓] Datos exportados exitosamente a '{nombre_csv}' usando Pandas.")