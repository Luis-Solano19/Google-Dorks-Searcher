from dotenv import load_dotenv, set_key
import os
from googlesearch import GoogleSearch
import argparse
import sys
from results_parser import ResultsParser

def env_config():
    """
        Configura el archivo .env con los valores proporcionados
    """
    api_key = input("Introduce tu API KEY: ")
    engine_id = input("Introduce tu engine ID: ")

    # En caso que .env no exista lo crea, luego crea la variable de entorno y le asigna el valor
    set_key(".env", "GOOGLE_KEY", api_key)
    set_key(".env", "SEARCH_ENGINE_ID", engine_id)


def main(query, configure_env, start_page, pages, lang, output_json, output_html):
    # Comprobar si existe el fichero/archivo de configuracion
    env_exists = os.path.exists(".env")

    if not env_exists or configure_env:
        env_config()
        print("Arhivo .env configurado satisfactoriamente.")
 
        # Parar la ejecucion luego de configurar el archivo.
        sys.exit(1)
    

    # Cargar variables en el entorno
    load_dotenv()

    # Leer API (max 100 requests por dia)
    GOOGLE_KEY = os.getenv("GOOGLE_KEY")

    # Leer Search Engine ID
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    if not query:
        print("Indica una consulta con el comando -q o --query , -h para ver la ayuda")
        sys.exit(1)
    
    gsearch = GoogleSearch(google_api=GOOGLE_KEY, google_engine_id=SEARCH_ENGINE_ID)

    results = gsearch.search(query=query, start_page=start_page, pages=pages, lang=lang)

    rparser = ResultsParser(resultados=results)
    # Mostar resultados en consola
    rparser.mostrar_consola()

    if output_html:
        rparser.export_html(output_html)
    
    if output_json:
        rparser.export_json(output_json)


if __name__ == "__main__":
    # Configuracion de los args del programa
    parser = argparse.ArgumentParser(description="Esta herramienta permite realizar hacking con buscadores de forma automatica")

    parser.add_argument("-q", "--query", type=str, 
        help="Especifica el dork/consulta a buscar. \nEjemplos: -q \"League of legends\" o --query  'filetype:sql \"MySQL dump\" (pass|password|passwd|pwd)' ")
    
    parser.add_argument("-c", "--config", action="store_true", 
        help="Inicia el proceso de config del archivo .env \nUtiliza esta opcion sin otros argumentos para configurar las claves.")

    parser.add_argument("--start_page", type=int, default=1, 
        help="Indica la pagina de inicio del buscador para los resultados (1 default)")
    
    parser.add_argument("--pages", type=int,default=1, 
        help="Indica el numero de paginas de resultados a obtener con la busqueda.")

    parser.add_argument("--lang", type=str, default="lang_es", 
        help="Codigo de idioma para los resultados de busqueda. 'lang_es' por defecto. ")

    parser.add_argument("--json", type=str, help="Exporta los resultados a JSON al fichero especificado\n Ejemplo: python ninjadorks.py -q 'filetype:sql \"MySQL dump\" (pass|password|passwd|pwd)' --json \"sql_passw.json\"")

    parser.add_argument("--html", type=str, help="Exporta los resultados a HTML al fichero especificado\n Ejemplo: python ninjadorks.py -q 'filetype:sql \"MySQL dump\" (pass|password|passwd|pwd)' --html \"sql_passw.html\" ")
    
    # Procesar argumentos
    args = parser.parse_args()


    main(query=args.query, configure_env=args.config, 
        start_page=args.start_page, pages=args.pages, 
        lang=args.lang, output_html=args.html, 
        output_json=args.json
    )