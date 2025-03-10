import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Imports do Core
from recon.core.utils import normalize_domain, resolve_ip
from recon.report.builder import ReportBuilder

# Imports dos Módulos (Formato explícito para evitar circular imports)
import recon.modules.internetdb as internetdb 
import recon.modules.crtsh as crtsh 
import recon.modules.hackertarget as hackertarget
import recon.modules.headers as headers
import recon.modules.reputation as reputation
import recon.modules.ssllabs as ssllabs
import recon.modules.observatory as observatory


console = Console()

def run_module(name, module_func, domain, ip):
    """
    Wrapper para execução segura dos módulos.
    Chama a função run() dentro de cada módulo.
    """
    try:
        # Chama a função run dentro do módulo (e.g., crtsh.run)
        return name, module_func.run(domain, ip)
    except Exception as e:
        # Em caso de crash do código do módulo, retorna erro limpo
        return name, {"error": str(e), "crash": True}

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

    # 3. Configuração dos Módulos
    # Lista de tuplas: (Nome Chave no JSON, Módulo Importado)
    modules_to_run = [
        ("internetdb", internetdb),
        ("crtsh", crtsh),
        ("hackertarget", hackertarget),
        ("headers", headers),
        ("reputation", reputation),
        ("ssllabs", ssllabs),
        ("observatory", observatory)
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
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submete tarefas
            futures = []
            for name, module in modules_to_run:
                # Passamos o objeto do módulo para run_module
                futures.append(executor.submit(run_module, name, module, domain, ip))

            # Coleta resultados
            for future in futures:
                name, data = future.result()
                
                # Roteamento dos dados para a categoria correta no JSON
                if name in ["crtsh", "hackertarget"]:
                    final_results["passive_recon"][name] = data
                elif name == "internetdb":
                    final_results["reputation"]["shodan_internetdb"] = data
                elif name == "reputation":
                    # reputation é o módulo que contém AbuseIPDB e GreyNoise
                    final_results["reputation"].update(data)
                elif name == "headers":
                    final_results["headers"] = data
                elif name in ["ssllabs", "observatory"]:
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