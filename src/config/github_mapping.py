"""
Configuración de búsquedas para GitHub.
Siempre devuelve una lista de queries.
"""
from typing import List

# ============ LENGUAJES ============
# La mayoría se usa como: language:{nombre}
# Solo excepciones donde el nombre en GitHub es diferente
LANGUAGE_EXCEPTIONS = {
    "C#": "C#",
    "C++": "C++",
    "Visual Basic (.Net)": "Visual Basic .NET",
    "Bash/Shell": "Shell",
    "HTML/CSS": None,  # Caso especial: se maneja abajo
}

# Lenguajes que funcionan con language:{nombre} tal cual
LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust",
    "C", "Ruby", "Swift", "Kotlin", "PHP",
    "SQL", "PowerShell", "Lua", "Assembly", "Dart", "R",
    "Groovy", "MATLAB", "Perl", "GDScript", "Elixir", "Scala",
    "Delphi", "Lisp", "Zig", "Erlang", "Fortran", "Ada",
    "F#", "OCaml", "Gleam", "Prolog", "COBOL", "Mojo",
    "MicroPython"
]

# ============ TOPICS (frameworks, herramientas, etc) ============
TOPIC_MAPPING = {
    # Frameworks Frontend
    "React": "react",
    "Vue.js": "vuejs",
    "Angular": "angular",
    "AngularJS": "angularjs",
    "Next.js": "nextjs",
    "Nuxt.js": "nuxtjs",
    "Svelte": "svelte",
    "jQuery": "jquery",
    "Astro": "astro",
    
    # Frameworks Backend
    "Django": "django",
    "Flask": "flask",
    "FastAPI": "fastapi",
    "Spring Boot": "spring-boot",
    "ASP.NET Core": "aspnet-core",
    "ASP.NET": "aspnet",
    "Blazor": "blazor",
    "Express": "expressjs",
    "NestJS": "nestjs",
    "Fastify": "fastify",
    "Ruby on Rails": "ruby-on-rails",
    "Symfony": "symfony",
    "Laravel": "laravel",
    "WordPress": "wordpress",
    "Drupal": "drupal",
    "Phoenix": "phoenix-framework",
    "Axum": "axum",
    
    # Herramientas y plataformas
    "Docker": "docker",
    "Kubernetes": "kubernetes",
    "Podman": "podman",
    "Terraform": "terraform",
    "Ansible": "ansible",
    "Prometheus": "prometheus",
    "Elasticsearch": "elasticsearch",
    "Splunk": "splunk",
    "Datadog": "datadog",
    "New Relic": "newrelic",
    
    # Bases de datos
    "PostgreSQL": "postgresql",
    "MySQL": "mysql",
    "SQLite": "sqlite",
    "MongoDB": "mongodb",
    "Redis": "redis",
    "Cassandra": "cassandra",
    "Neo4J": "neo4j",
    "Dynamodb": "dynamodb",
    "Firebase": "firebase",
    "Supabase": "supabase",
    "Cosmos DB": "azure-cosmos-db",
    "Snowflake": "snowflake",
    "BigQuery": "google-bigquery",
    "InfluxDB": "influxdb",
    "DuckDB": "duckdb",
    "Clickhouse": "clickhouse",
    "IBM DB2": "db2",
    "Amazon Redshift": "amazon-redshift",
    "Oracle": "oracle-database",
    "Microsoft SQL Server": "sql-server",
    "MariaDB": "mariadb",
    "Cockroachdb": "cockroachdb",
    "Datomic": "datomic",
    "H2": "h2-database",
    "Valkey": "valkey",
    "Pocketbase": "pocketbase",
    "Cloud Firestore": "cloud-firestore",
    "Firebase Realtime Database": "firebase-realtime-database",
    
    # Paquetes y build tools
    "npm": "npm",
    "Yarn": "yarn",
    "pnpm": "pnpm",
    "Bun": "bun",
    "Pip": "pip",
    "Poetry": "poetry",
    "Maven": "maven",
    "Gradle": "gradle",
    "Cargo": "cargo",
    "Composer": "composer",
    "NuGet": "nuget",
    "MSBuild": "msbuild",
    "Make": "makefile",
    "Ninja": "ninja-build",
    "APT": "apt",
    "Homebrew": "homebrew",
    "Chocolatey": "chocolatey",
    "Pacman": "pacman",
    "Webpack": "webpack",
    "Vite": "vite",
    
    # Servicios cloud
    "Amazon Web Services (AWS)": "aws",
    "Microsoft Azure": "azure",
    "Google Cloud": "google-cloud",
    "Cloudflare": "cloudflare",
    "Digital Ocean": "digitalocean",
    "Vercel": "vercel",
    "Netlify": "netlify",
    "Heroku": "heroku",
    "Deno": "deno",
    "Railway": "railway",
    "IBM Cloud": "ibm-cloud",
    "Yandex Cloud": "yandex-cloud",
    "Databricks SQL": "databricks",
}

# ============ BÚSQUEDA LIBRE (modelos de IA, etc) ============
SEARCH_MAPPING = {
    "openAI GPT (chatbot models)": "openai gpt",
    "openAI Reasoning models": "openai reasoning",
    "openAI Image generating models": "openai image generation",
    "Anthropic: Claude Sonnet": "claude sonnet",
    "Gemini (Flash general purpose models)": "gemini flash",
    "Gemini (Pro Reasoning models)": "gemini pro",
    "DeepSeek (R- Reasoning models)": "deepseek reasoning",
    "DeepSeek (V- General purpose models)": "deepseek",
    "Meta Llama (all models)": "llama",
    "Mistral AI models": "mistral",
    "X Grok models": "grok xai",
    "Alibaba Cloud Qwen models": "qwen",
    "Microsoft Phi-4 models": "phi-4",
    "Cohere: Command A": "cohere command",
    "Reka (Flash 3 or other Reka models)": "reka",
    "Perplexity Sonar models": "perplexity sonar",
    "Amazon Titan models": "amazon titan",
    "Microsoft Access": "microsoft access",
}

# ============ FUNCIONES PÚBLICAS ============

def build_github_queries(technology: str) -> List[str]:
    """
    Construye las queries de GitHub para una tecnología.
    SIEMPRE devuelve una lista, incluso si es una sola query.
    
    Args:
        technology: Nombre de la tecnología
        
    Returns:
        Lista de queries para la API de GitHub
    """
    # 1. Caso especial: HTML/CSS
    if technology == "HTML/CSS":
        return ["language:HTML", "language:CSS"]
    
    # 2. Búsqueda libre (modelos de IA)
    if technology in SEARCH_MAPPING:
        return [SEARCH_MAPPING[technology]]
    
    # 3. Topic (frameworks, herramientas, etc)
    if technology in TOPIC_MAPPING:
        return [f"topic:{TOPIC_MAPPING[technology]}"]
    
    # 4. Lenguajes
    if technology in LANGUAGES:
        return [f"language:{technology}"]
    
    # 5. Lenguajes con excepción
    if technology in LANGUAGE_EXCEPTIONS:
        lang = LANGUAGE_EXCEPTIONS[technology]
        if lang:
            return [f"language:{lang}"]
    
    # 6. Si no está mapeado, devolver lista vacía
    return []


def get_all_technologies() -> List[str]:
    """
    Devuelve todas las tecnologías mapeadas, en orden y sin duplicados.
    """
    technologies = []
    
    # Mantener orden: primero lenguajes, luego topics, luego search
    technologies.extend(LANGUAGES)
    technologies.extend(list(LANGUAGE_EXCEPTIONS.keys()))
    technologies.extend(list(TOPIC_MAPPING.keys()))
    technologies.extend(list(SEARCH_MAPPING.keys()))
    
    # Eliminar duplicados manteniendo orden
    return list(dict.fromkeys(technologies))