import random
import time
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN Y CATÁLOGO DE DATOS (Basado en la tabla transacciones_gemas)
# ==============================================================================
MOTIVOS_CONFIG = [
    {
        'motivo': 'compra',
        'rango_gemas': (100, 2000),
        'requiere_referencia': True
    },
    {
        'motivo': 'bono_diario',
        'rango_gemas': (10, 50),
        'requiere_referencia': False
    },
    {
        'motivo': 'recompensa_personaje',
        'rango_gemas': (25, 150),
        'requiere_referencia': True
    }
]

def generar_transaccion(id_transaccion_actual):
    """
    Genera un registro simulado con las columnas de 'transacciones_gemas'.
    """
    # 1. Simulación de usuario (IDs entre 1 y 50)
    id_usuario = random.randint(1, 50)

    # 2. Selección de motivo
    config_motivo = random.choice(MOTIVOS_CONFIG)
    motivo = config_motivo['motivo']

    # 3. Cantidad de gemas
    cantidad = random.randint(*config_motivo['rango_gemas'])

    # 4. id_referencia (puede ser None o un ID bigint)
    if config_motivo['requiere_referencia'] and random.random() > 0.20:
        id_referencia = random.randint(100000, 999999)
    else:
        id_referencia = None

    # 5. Fecha actual con timestamp
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'id_transaccion': id_transaccion_actual,
        'id_usuario': id_usuario,
        'cantidad': cantidad,
        'motivo': motivo,
        'id_referencia': id_referencia,
        'fecha': fecha
    }

def simular_transacciones(limite=20, intervalo_segundos=(0.5, 1.5)):
    """
    Ejecuta el bucle de simulación en tiempo real.
    - limite: Cantidad de eventos a simular (None para infinito hasta Ctrl+C).
    - intervalo_segundos: Rango de espera entre cada evento generado.
    """
    print("=" * 70)
    print("  SIMULADOR: transacciones_gemas")
    print("=" * 70)

    contador = 0

    try:
        while True:
            contador += 1
            transaccion = generar_transaccion(id_transaccion_actual=contador)

            # Imprimir salida de la transacción
            print(f"[#{transaccion['id_transaccion']:04d}] "
                  f"Usuario: {transaccion['id_usuario']:2d} | "
                  f"Gemas: +{transaccion['cantidad']:4d} | "
                  f"Motivo: {transaccion['motivo']:<20} | "
                  f"Ref: {str(transaccion['id_referencia']):<6} | "
                  f"Fecha: {transaccion['fecha']}")

            # Detener si se especificó un límite
            if limite and contador >= limite:
                print(f"\n[✓] Simulación completada. Total generados: {contador}")
                break

            # Pausa simulando tiempo real
            time.sleep(random.uniform(*intervalo_segundos))

    except KeyboardInterrupt:
        print("\n[!] Simulación detenida manualmente por el usuario.")

# ==============================================================================
# EJECUCIÓN
# ==============================================================================
if __name__ == '__main__':
    # Configuración: 20 registros con pausas de 0.5 a 1.5 segundos
    simular_transacciones(limite=20, intervalo_segundos=(0.5, 1.5))