from dotenv import load_dotenv
import os
from googlesearch import GoogleSearch

def main():
    # Cargar variables en el entorno
    load_dotenv()

    # Leer API (max 100 requests por dia)
    GOOGLE_KEY = os.getenv("GOOGLE_KEY")

    # Leer Search Engine ID
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    query = 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'

    gsearch = GoogleSearch(google_api=GOOGLE_KEY, google_engine_id=SEARCH_ENGINE_ID)

    results = gsearch.search(query=query)

    print(results)


if __name__ == "__main__":
    main()