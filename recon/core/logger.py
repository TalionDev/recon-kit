"""
Módulo de logging estruturado para o Recon-Kit.
"""
import logging


def setup_logger(name: str, level=logging.INFO):
    """
    Configura e retorna um logger com formatação padrão.
    
    Args:
        name: Nome do logger (geralmente __name__ do módulo)
        level: Nível de logging (default: INFO)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evita adicionar handlers duplicados
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger
