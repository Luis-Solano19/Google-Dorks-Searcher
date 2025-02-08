import requests

class GoogleSearch:
    def __init__(self, google_api, google_engine_id):
        """
            Inicializar una nueva instancia de GoogleSearch.
            Permite realizar peticiones automatizadas a la API de Google.
            google_api (str): Clave API de Google
            google_engine_id (str): Id del motor de busqueda custom de Google.
        """
        self.api_key = google_api
        self.engine_id = google_engine_id

    def search(self, query, start_page=1, pages=1, lang="lang_es"):
        """
            Realizar busqueda en google, utilizando su API.
            query (str): Algo a buscar
            start_page (int): Pagina de inicio - default 1
            pages (int): Paginas extras de las cuales obtener resultados - default 1
            lang (str): Lenguaje, por defecto es espanol (lang_es)
        """
        final_results = []

        results_per_page = 10 # Google por defecto muestra 10 resultados por pagina.

        for page in range(pages):
            """
                Calculates the index or num of result from which we start looking, E.g if starting page = 2, 
                starting_result is gonna be  = 11 so we get results from 11-21, 
                then for next page is gonna be 22 - 32 and so on and so forth.
            """

            # Calcular el indice de la pagina (num de resultado) por el cual iniciar
            starting_result = (start_page - 1) * results_per_page + 1 + (page * results_per_page) 
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={starting_result}&lr={lang}"
            response = requests.get(url)

            # Comprobar si la respuesta es correcta o [200]
            if response.status_code == 200:
                data = response.json()
                results = data.get("items")

                # Dar formato a resultados
                cresults = self.custom_results(results=results)

                # Ya formateados, se adjuntan a resultados finales
                # Extend adjuna multiples objetos, para que al final, no se tenga en la lista algo asi: [ [], [] ]
                final_results.extend(cresults)
                
            else:
                print(f"Error al consultar la pagina: {page}: HTTP {response.status_code}")
                break # Romper la iteracion
        
        return final_results
        
            
    
    def custom_results(self, results):
        """
            Filtra los resultados obtenidos. En este caso devuelve titulo, contenido, link
        """
        custom_results = []
        for r in results:
            cresult = {}
            cresult["title"] = r.get("title")
            cresult["description"] = r.get("snippet")
            cresult["link"] = r.get("link")
            custom_results.append(cresult)
        
        return custom_results