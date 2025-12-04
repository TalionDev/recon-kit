import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Imports do Core
from recon.core.utils import normalize_domain, resolve_ip
from recon.report.builder import ReportBuilder
from recon.config import MAX_WORKERS

# Imports dos Módulos (Classes)
from recon.modules.internetdb import InternetdbModule
from recon.modules.crtsh import CrtshModule
from recon.modules.hackertarget import HackertargetModule
from recon.modules.headers import HeadersModule
from recon.modules.reputation import ReputationModule
from recon.modules.ssllabs import SsllabsModule
from recon.modules.observatory import ObservatoryModule


console = Console()

def run_module(module_instance, domain, ip):
    """
    Wrapper para execução segura dos módulos.
    Chama o método run() da instância do módulo.
    """
    try:
        return module_instance.NAME, module_instance.CATEGORY, module_instance.run(domain, ip)
    except Exception as e:
        # Em caso de crash do código do módulo, retorna erro limpo
        return module_instance.NAME, module_instance.CATEGORY, {"error": str(e), "crash": True}

def main():
    # 1. Setup CLI
    parser = argparse.ArgumentParser(description="Recon-Kit - Passive OSINT Scanner")
    parser.add_argument("--domain", required=True, help="Domínio alvo (ex: exemplo.com)")
    args = parser.parse_args()

    # Cabeçalho Bonito (NOME DO PROJETO ATUALIZADO)
    console.print(Panel.fit("[bold cyan]Recon-Kit[/bold cyan] [white]Recon-Kit[/white]", border_style="cyan"))

    # 2. Pré-processamento
    domain = normalize_domain(args.domain)
    console.print(f"[bold]Alvo:[/bold] {domain}")

    ip = resolve_ip(domain)
    if not ip:
        console.print("[bold red]Erro Crítico:[/bold red] Não foi possível resolver o IP do domínio.")
        console.print("O scanner precisa do IP para módulos de reputação e Shodan.")
        sys.exit(1)
    
    console.print(f"[bold green] IP Resolvido:[/bold green] {ip}\n")

    # 3. Configuração dos Módulos (instâncias)
    modules_to_run = [
        InternetdbModule(),
        CrtshModule(),
        HackertargetModule(),
        HeadersModule(),
        ReputationModule(),
        SsllabsModule(),
        ObservatoryModule()
    ]

    # Estrutura Final dos Dados
    final_results = {
        "resolved_ip": ip,
        "domain": domain,
        "passive_recon": {}, # crtsh, hackertarget
        "reputation": {},    # internetdb, reputation (greynoise/abuseipdb)
        "headers": {},       # headers
        "https": {}          # ssllabs, observatory
    }

    # 4. Execução Paralela
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Escaneando fontes passivas...", total=len(modules_to_run))
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submete tarefas
            futures = []
            for module in modules_to_run:
                futures.append(executor.submit(run_module, module, domain, ip))

            # Coleta resultados
            for future in futures:
                name, category, data = future.result()
                
                # Roteamento automático dos dados baseado na CATEGORY do módulo
                if category == "passive_recon":
                    final_results["passive_recon"][name] = data
                elif category == "reputation":
                    if name == "internetdb":
                        final_results["reputation"]["shodan_internetdb"] = data
                    elif name == "reputation":
                        # reputation é o módulo que contém AbuseIPDB e GreyNoise
                        final_results["reputation"].update(data)
                    else:
                        final_results["reputation"][name] = data
                elif category == "headers":
                    final_results["headers"] = data
                elif category == "https":
                    final_results["https"][name] = data
                
                progress.advance(task)

    # 5. Exportação
    console.print("\n[bold blue] Gerando relatórios...[/bold blue]")
    builder = ReportBuilder(domain, final_results)
    
    json_path = builder.save_json()
    md_path = builder.save_markdown()

    console.print(f"[green]✔ Scan Finalizado![/green]")
    console.print(f" JSON: [underline]{json_path}[/underline]")
    console.print(f" Report: [underline]{md_path}[/underline]")

if __name__ == "__main__":
    main()