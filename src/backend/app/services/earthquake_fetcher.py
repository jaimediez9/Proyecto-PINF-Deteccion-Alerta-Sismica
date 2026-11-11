import httpx

ROA_URL = "La url del ROA cuando nos la den"

#esta función os dará los terremotos almacenados en el web server del roa
#Faltan concretar algunos puntos; ahora mismo asume que se le devolverá una lista de JSON
#Yo completaré esta función cuando tengamos todos los datos, la podéis usar como abstracción
def fetch_earthquakes():

    try:
        response = httpx.get(ROA_URL, timeout=15)

        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException:
        print("El servidor del ROA ha tardado demasiado en responder.")

    except httpx.HTTPStatusError as error:
        print(f"El servidor ha devuelto un error: {error.response.status_code}")

    except httpx.RequestError as error:
        print(f"Error de conexión con el ROA: {error}")

    except ValueError:
        print("La respuesta del servidor no contiene un JSON válido.")

    return None