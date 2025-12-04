"""
Classe base abstrata para todos os módulos do Recon-Kit.
Define o contrato que todos os módulos devem seguir.
"""
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """
    Classe base abstrata que define o contrato dos módulos.
    
    Atributos de classe:
        CATEGORY: Categoria do módulo (passive_recon, reputation, headers, https)
        NAME: Nome identificador do módulo
    """
    CATEGORY = "unknown"
    NAME = "base"
    
    def __init__(self, fetcher=None):
        """
        Inicializa o módulo com um Fetcher.
        
        Args:
            fetcher: Instância do Fetcher (opcional, usa singleton se não fornecido)
        """
        from recon.core.fetcher import Fetcher
        self.fetcher = fetcher or Fetcher.get_instance()
    
    @abstractmethod
    def run(self, domain: str, ip: str | None) -> dict:
        """
        Executa a lógica principal do módulo.
        
        Args:
            domain: Domínio alvo
            ip: Endereço IP resolvido (pode ser None)
        
        Returns:
            Dicionário com os resultados do módulo
        """
        pass
    
    def error_response(self, error_type: str, message: str) -> dict:
        """
        Retorna uma resposta de erro padronizada.
        
        Args:
            error_type: Tipo/código do erro
            message: Mensagem descritiva do erro
        
        Returns:
            Dicionário com informações do erro
        """
        return {
            "success": False,
            "error_type": error_type,
            "message": message
        }
