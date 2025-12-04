import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from recon.config import DEFAULT_HEADERS, TIMEOUT, MAX_RETRIES, VERIFY_SSL
import urllib3

# Suprimir avisos de SSL inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Fetcher:
    """
    Cliente HTTP centralizado com tratamento de erros, retries e headers consistentes.
    Implementa padrão Singleton para evitar múltiplas instâncias.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Retorna a instância singleton do Fetcher."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        
        # Estratégia de Retry: Tenta 3 vezes em caso de erros de servidor ou rate limit
        retries = Retry(
            total=MAX_RETRIES,
            backoff_factor=1, # Espera 1s, 2s, 4s...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url, params=None, timeout=TIMEOUT):
        """Executa GET seguro."""
        try:
            response = self.session.get(
                url, 
                params=params, 
                timeout=timeout, 
                verify=VERIFY_SSL
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            return None

    def get_json(self, url, params=None):
        """Executa GET e tenta parsear JSON automaticamente."""
        resp = self.get(url, params)
        if resp:
            try:
                # Trata casos onde a API retorna texto vazio ou HTML de erro disfarçado
                if not resp.content: 
                    return None
                return resp.json()
            except ValueError:
                return None
        return None

    def head(self, url, timeout=TIMEOUT):
        """Executa HEAD (apenas headers, sem corpo) para ser stealthy."""
        try:
            return self.session.head(
                url, 
                timeout=timeout, 
                verify=VERIFY_SSL,
                allow_redirects=True
            )
        except requests.exceptions.RequestException:
            return None