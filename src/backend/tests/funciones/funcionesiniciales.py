from terremotos import terremotos
from datetime import datetime

def terremotos_anteriores(terremotos, fecha_hora):
    anteriores = []

    fecha_busqueda = datetime.strptime(
        fecha_hora, "%Y-%m-%d %H:%M:%S"
    )

    for terremoto in terremotos:
        fecha_terremoto= datetime.strptime(
            terremoto["fecha"] + " " + terremoto["hora"],
            "%Y-%m-%d %H:%M:%S"
        )

        if fecha_terremoto < fecha_busqueda:
            anteriores.append(terremoto)

    return anteriores

def terremotos_posteriores(terremotos, fecha_hora, n):

    posteriores=[]

    fecha_busqueda = datetime.strptime(
        fecha_hora, "%Y-%m-%d %H:%M:%S"
    )

    for terremoto in terremotos:
        fecha_terremoto = datetime.strptime(
            terremoto["fecha"] + " " + terremoto["hora"],
            "%Y-%m-%d %H:%M:%S"
        )

        if fecha_terremoto > fecha_busqueda:
            posteriores.append(terremoto)

    posteriores.sort(
        key=lambda t: datetime.strptime(
            terremoto["fecha"] + " " + terremoto["hora"],
            "%Y-%m-%d %H:%M:%S"
        )
    )
    return posteriores[:n]


fecha = "2026-11-11 10:40:00"
print("TERREMOTOS ANTERIORES:")

resultado = terremotos_anteriores(terremotos , fecha)

for t in resultado:
    print(t["id"], t["fecha"], t["hora"])

print("\nTERREMOTOS POSTERIORES:")

resultado = terremotos_posteriores(terremotos, fecha, 2)

for t in resultado:
    print(t["id"], t["fecha"], t["hora"])

