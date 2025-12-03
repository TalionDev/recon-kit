
# Recon-Kit

Recon-Kit é um conjunto de ferramentas de reconhecimento passivo para auxiliar análises iniciais de segurança e mapeamento de superfície de ataque. Todo o processo utiliza apenas fontes públicas e endpoints de consultas legítimas, sem agressividade, sem tentativa de exploração e sem envio de cargas maliciosas.

O objetivo do projeto é consolidar informações essenciais obtidas de forma passiva e organizada, servindo como uma etapa de footprinting inicial. Ele permite agrupar dados como subdomínios, informações DNS, postura de segurança HTTPS, reputação do IP alvo, CVEs conhecidos associados ao IP e detalhes derivados de certificados públicos.

O projeto é modular, expansível e orientado a bibliotecas independentes para facilitar contribuições e adições de novos endpoints públicos.

Se você tiver sugestões de módulos, endpoints adicionais ou melhorias na arquitetura interna, é bem-vindo a contribuir.

## Estrutura

A estrutura principal do projeto é dividida entre núcleo, módulos e relatórios.

```text
recon/
    main.py
    config.py
    core/
        __init__.py
        fetcher.py
        utils.py
    modules/
        __init__.py
        crtsh.py
        hackertarget.py
        internetdb.py
        headers.py
        reputation.py
        ssllabs.py
        observatory.py
    report/
        __init__.py
        builder.py

results/
    (arquivos de saída gerados automaticamente em JSON e Markdown)

requirements.txt
```


## Categorias de Funcionamento
O projeto é separado em grupos lógicos para refletir camadas clássicas do processo de OSINT e fingerprinting:

### 1. Fingerprinting via certificados
crt.sh: Coleta subdomínios históricos e ativos derivados de certificados públicos.

### 2. Footprinting de DNS
hackertarget: Consulta pública para registros DNS básicos como A, MX, NS e SOA.

### 3. Reputação
internetdb (Shodan Community): Fornece portas observadas, CPEs associados e CVEs vinculadas ao IP.

reputation (GreyNoise Community, AbuseIPDB): Classifica o IP quanto a ruído e reputação pública.

### 4. Postura HTTPS
ssllabs (cache mode): Coleta dados de certificados, versão de TLS e notas de segurança.

observatory (Mozilla): Obtém notas de segurança HTTP no modo cache.

### 5. Fingerprinting de headers
headers: Coleta headers básicos e analisa níveis de segurança HTTP.

## Uso


#python -m recon.main.py --domain exemplo.com

Os resultados serão exportados para results/exemplo.com.json e results/exemplo.com.md.

Ambiente
Instale as dependências com:

#pip install -r requirements.txt

## Contribuições

Envie sugestões de módulos, endpoints públicos adicionais ou ajustes na arquitetura. Solicitações de melhoria são bem-vindas.
