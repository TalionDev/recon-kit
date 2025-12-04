"""
Testes básicos para os módulos do Recon-Kit.
"""
import pytest
from unittest.mock import Mock, patch


class TestFetcherSingleton:
    """Testes para o padrão singleton do Fetcher."""
    
    def test_fetcher_singleton(self):
        """Verifica que get_instance retorna a mesma instância."""
        from recon.core.fetcher import Fetcher
        
        # Reset singleton para teste isolado
        Fetcher._instance = None
        
        f1 = Fetcher.get_instance()
        f2 = Fetcher.get_instance()
        assert f1 is f2
    
    def test_fetcher_singleton_after_reset(self):
        """Verifica que reset cria nova instância."""
        from recon.core.fetcher import Fetcher
        
        Fetcher._instance = None
        f1 = Fetcher.get_instance()
        
        Fetcher._instance = None
        f2 = Fetcher.get_instance()
        
        assert f1 is not f2


class TestBaseModule:
    """Testes para a classe base abstrata."""
    
    def test_error_response_format(self):
        """Verifica formato padronizado de erro."""
        from recon.modules.crtsh import CrtshModule
        
        module = CrtshModule()
        error = module.error_response("TEST_ERROR", "Test message")
        
        assert error["success"] is False
        assert error["error_type"] == "TEST_ERROR"
        assert error["message"] == "Test message"
    
    def test_module_uses_fetcher_singleton(self):
        """Verifica que módulos usam o singleton do Fetcher."""
        from recon.core.fetcher import Fetcher
        from recon.modules.crtsh import CrtshModule
        
        Fetcher._instance = None
        module = CrtshModule()
        
        assert module.fetcher is Fetcher.get_instance()


class TestModuleCategories:
    """Testes para verificar categorias dos módulos."""
    
    def test_crtsh_category(self):
        from recon.modules.crtsh import CrtshModule
        assert CrtshModule.CATEGORY == "passive_recon"
        assert CrtshModule.NAME == "crtsh"
    
    def test_hackertarget_category(self):
        from recon.modules.hackertarget import HackertargetModule
        assert HackertargetModule.CATEGORY == "passive_recon"
        assert HackertargetModule.NAME == "hackertarget"
    
    def test_internetdb_category(self):
        from recon.modules.internetdb import InternetdbModule
        assert InternetdbModule.CATEGORY == "reputation"
        assert InternetdbModule.NAME == "internetdb"
    
    def test_headers_category(self):
        from recon.modules.headers import HeadersModule
        assert HeadersModule.CATEGORY == "headers"
        assert HeadersModule.NAME == "headers"
    
    def test_reputation_category(self):
        from recon.modules.reputation import ReputationModule
        assert ReputationModule.CATEGORY == "reputation"
        assert ReputationModule.NAME == "reputation"
    
    def test_ssllabs_category(self):
        from recon.modules.ssllabs import SsllabsModule
        assert SsllabsModule.CATEGORY == "https"
        assert SsllabsModule.NAME == "ssllabs"
    
    def test_observatory_category(self):
        from recon.modules.observatory import ObservatoryModule
        assert ObservatoryModule.CATEGORY == "https"
        assert ObservatoryModule.NAME == "observatory"


class TestModulesRequireIP:
    """Testes para módulos que requerem IP."""
    
    def test_internetdb_requires_ip(self):
        from recon.modules.internetdb import InternetdbModule
        
        module = InternetdbModule()
        result = module.run("example.com", None)
        
        assert result["success"] is False
        assert result["error_type"] == "NO_IP"
    
    def test_reputation_requires_ip(self):
        from recon.modules.reputation import ReputationModule
        
        module = ReputationModule()
        result = module.run("example.com", None)
        
        assert result["success"] is False
        assert result["error_type"] == "NO_IP"


class TestBackwardCompatibility:
    """Testes de compatibilidade retroativa."""
    
    def test_crtsh_run_function_exists(self):
        """Verifica que função run() existe para compatibilidade."""
        from recon.modules import crtsh
        assert hasattr(crtsh, 'run')
        assert callable(crtsh.run)
    
    def test_hackertarget_run_function_exists(self):
        from recon.modules import hackertarget
        assert hasattr(hackertarget, 'run')
        assert callable(hackertarget.run)
    
    def test_internetdb_run_function_exists(self):
        from recon.modules import internetdb
        assert hasattr(internetdb, 'run')
        assert callable(internetdb.run)
    
    def test_headers_run_function_exists(self):
        from recon.modules import headers
        assert hasattr(headers, 'run')
        assert callable(headers.run)
    
    def test_reputation_run_function_exists(self):
        from recon.modules import reputation
        assert hasattr(reputation, 'run')
        assert callable(reputation.run)
    
    def test_ssllabs_run_function_exists(self):
        from recon.modules import ssllabs
        assert hasattr(ssllabs, 'run')
        assert callable(ssllabs.run)
    
    def test_observatory_run_function_exists(self):
        from recon.modules import observatory
        assert hasattr(observatory, 'run')
        assert callable(observatory.run)


class TestConfig:
    """Testes para configurações."""
    
    def test_new_config_constants_exist(self):
        from recon import config
        
        assert hasattr(config, 'MAX_WORKERS')
        assert hasattr(config, 'MAX_SUBDOMAINS')
        assert hasattr(config, 'CACHE_ENABLED')
        assert hasattr(config, 'CACHE_TTL')
        assert hasattr(config, 'OUTPUT_DIR')
    
    def test_config_values(self):
        from recon import config
        
        assert config.MAX_WORKERS == 5
        assert config.MAX_SUBDOMAINS == 100
        assert config.CACHE_ENABLED is False
        assert config.CACHE_TTL == 3600
        assert config.OUTPUT_DIR == "results"


class TestLogger:
    """Testes para o módulo de logging."""
    
    def test_setup_logger_returns_logger(self):
        from recon.core.logger import setup_logger
        import logging
        
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)
    
    def test_setup_logger_with_custom_level(self):
        from recon.core.logger import setup_logger
        import logging
        
        logger = setup_logger("test_debug_logger", level=logging.DEBUG)
        assert logger.level == logging.DEBUG


class TestUtils:
    """Testes para funções utilitárias."""
    
    def test_resolve_all_ips_returns_list(self):
        from recon.core.utils import resolve_all_ips
        
        # Testando com domínio inválido retorna lista vazia
        result = resolve_all_ips("invalid.domain.that.does.not.exist.xyz")
        assert isinstance(result, list)
