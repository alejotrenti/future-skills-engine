# src/config/technology_mapping.py
"""
Technology mapping configuration for Future Skills Engine.
"""

import re

# ==========================
# BLACKLIST
# ==========================

IGNORE_TECHNOLOGIES = {
    "windows", "office", "excel", "visualstudio",
    "word", "powerpoint", "outlook", "sharepoint",
    "teams", "notepad", "paint", "calculator",
}


# ==========================
# FUNCIÓN DE LIMPIEZA
# ==========================

def clean_tech_name(text: str) -> str:
    """Limpia un nombre de tecnología para normalización."""
    if not text:
        return ""
    return re.sub(
        r"[^a-z0-9+.#-]",
        "",
        text.strip().lower()
    )


# ==========================
# ALIASES (en formato legible)
# ==========================

RAW_ALIASES = {
    # ==========================
    # LENGUAJES
    # ==========================
    "HTML": "html",
    "CSS": "css",
    "HTML/CSS": "html",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Python": "python",
    "Java": "java",
    "C#": "csharp",
    "C++": "cpp",
    "C": "c",
    "Rust": "rust",
    "Go": "go",
    "Golang": "go",
    "Kotlin": "kotlin",
    "Swift": "swift",
    "PHP": "php",
    "Ruby": "ruby",
    "Scala": "scala",
    "R": "r",
    "MATLAB": "matlab",
    "Julia": "julia",
    "Elixir": "elixir",
    "Clojure": "clojure",
    "Haskell": "haskell",
    "Perl": "perl",
    "Lua": "lua",
    "Dart": "dart",
    "Groovy": "groovy",
    "Objective-C": "objectivec",
    "VBA": "vba",
    "PowerShell": "powershell",
    "Bash": "bash",
    "Shell": "shell",
    "Zsh": "zsh",
    "Assembly": "assembly",
    
    # ==========================
    # RUNTIMES
    # ==========================
    "Node.js": "nodejs",
    "NodeJS": "nodejs",
    "Deno": "deno",
    "Bun": "bun",
    
    # ==========================
    # FRAMEWORKS
    # ==========================
    "React": "react",
    "React.js": "react",
    "ReactJS": "react",
    "Vue": "vue",
    "Vue.js": "vue",
    "VueJS": "vue",
    "Angular": "angular",
    "Angular.js": "angular",
    "AngularJS": "angular",
    "Svelte": "svelte",
    "jQuery": "jquery",
    "Next.js": "nextjs",
    "NextJS": "nextjs",
    "Gatsby": "gatsby",
    "Tailwind": "tailwind",
    "TailwindCSS": "tailwind",
    "Django": "django",
    "Flask": "flask",
    "FastAPI": "fastapi",
    "Spring": "spring",
    "Spring Boot": "springboot",
    "ASP.NET": "aspnet",
    "ASP.NET Core": "aspnetcore",
    "Laravel": "laravel",
    "Rails": "rails",
    "Ruby on Rails": "rails",
    "Express": "express",
    "Express.js": "express",
    "NestJS": "nestjs",
    "Astro": "astro",
    "SolidJS": "solidjs",
    "Remix": "remix",
    "Nuxt": "nuxt",
    "Axum": "axum",
    "Blade": "blade",
    
    # ==========================
    # BASES DE DATOS
    # ==========================
    "PostgreSQL": "postgresql",
    "Postgres": "postgresql",
    "MySQL": "mysql",
    "MongoDB": "mongodb",
    "Mongo": "mongodb",
    "Redis": "redis",
    "Elasticsearch": "elasticsearch",
    "Elastic": "elasticsearch",
    "Cassandra": "cassandra",
    "DynamoDB": "dynamodb",
    "SQLite": "sqlite",
    "MariaDB": "mariadb",
    "Oracle": "oracle",
    "SQL Server": "sqlserver",
    "Firebase": "firebase",
    "Firestore": "firestore",
    "Amazon Redshift": "redshift",
    "Redshift": "redshift",
    "BigQuery": "bigquery",
    "Snowflake": "snowflake",
    "DuckDB": "duckdb",
    "Polars": "polars",
    "Pandas": "pandas",
    "NumPy": "numpy",
    
    # ==========================
    # CLOUD Y DEVOPS
    # ==========================
    "Docker": "docker",
    "Dockerfile": "docker",
    "Kubernetes": "kubernetes",
    "K8s": "kubernetes",
    "Amazon Web Services": "aws",
    "Amazon Web Services (AWS)": "aws",
    "AWS": "aws",
    "Azure": "azure",
    "Microsoft Azure": "azure",
    "Google Cloud": "gcp",
    "Google Cloud Platform": "gcp",
    "GCP": "gcp",
    "Terraform": "terraform",
    "Ansible": "ansible",
    "Jenkins": "jenkins",
    "GitHub Actions": "githubactions",
    "GitLab CI": "gitlabci",
    "CircleCI": "circleci",
    "S3": "s3",
    "Amazon S3": "s3",
    "EC2": "ec2",
    "Amazon EC2": "ec2",
    "Lambda": "lambda",
    "AWS Lambda": "lambda",
    "RDS": "rds",
    "Amazon RDS": "rds",
    "Prometheus": "prometheus",
    "Grafana": "grafana",
    "Helm": "helm",
    "Nginx": "nginx",
    "Bicep": "bicep",
    
    # ==========================
    # ALIBABA
    # ==========================
    "Alibaba Cloud": "alibaba_cloud",
    "Alibaba Cloud Qwen": "alibaba_qwen",
    "Alibaba Cloud Qwen models": "alibaba_qwen",
    "Qwen": "alibaba_qwen",
    
    # ==========================
    # AI MODELS
    # ==========================
    "Gemini": "gemini",
    "Google Gemini": "gemini",
    "GitHub Copilot": "github_copilot",
    "Copilot": "github_copilot",
    "Claude 3": "claude",
    "Anthropic Claude": "claude",
    "Claude": "claude",
    "Mistral": "mistral",
    "DeepSeek": "deepseek",
    "DeepSeek R": "deepseek_reasoning",
    "Amazon Titan": "amazon_titan",
    "Amazon Titan models": "amazon_titan",
    "OpenAI": "openai",
    "OpenAI GPT": "openai_gpt",
    "GPT": "gpt",
    "Llama": "llama",
    
    # ==========================
    # AI/ML TECNOLOGÍAS
    # ==========================
    "TensorFlow": "tensorflow",
    "Tensorflow": "tensorflow",
    "PyTorch": "pytorch",
    "Keras": "keras",
    "Scikit-learn": "scikitlearn",
    "Scikit Learn": "scikitlearn",
    "OpenCV": "opencv",
    "Hugging Face": "huggingface",
    "HuggingFace": "huggingface",
    "LangChain": "langchain",
    
    # ==========================
    # BIG DATA
    # ==========================
    "Apache Spark": "spark",
    "Spark": "spark",
    "Hadoop": "hadoop",
    "Apache Hadoop": "hadoop",
    "Kafka": "kafka",
    "Apache Kafka": "kafka",
    "Airflow": "airflow",
    "Apache Airflow": "airflow",
    "dbt": "dbt",
    "Databricks": "databricks",
    
    # ==========================
    # BLOCKCHAIN
    # ==========================
    "Blockchain": "blockchain",
    "Ethereum": "ethereum",
    "Solidity": "solidity",
    "Web3": "web3",
    
    # ==========================
    # ARQUITECTURA E INTEGRACIÓN
    # ==========================
    "Serverless": "serverless",
    "Microservices": "microservices",
    "API": "api",
    "GraphQL": "graphql",
    "REST": "rest",
    "REST API": "rest",
    "Edge Computing": "edge_computing",
    "Quantum Computing": "quantum_computing",
    
    # ==========================
    # RESEARCH AREAS
    # ==========================
    "Machine Learning": "machine_learning",
    "Deep Learning": "deep_learning",
    "NLP": "nlp",
    "Computer Vision": "computer_vision",
    "Reinforcement Learning": "reinforcement_learning",
    "Generative AI": "generative_ai",
    "LLM": "llm",
    "RAG": "rag",
    
    # ==========================
    # OTROS
    # ==========================
    "Centreon": "centreon",
    "ANTLR": "antlr",
    "APT": "apt",
    "Batch": "batch",
    "BitBake": "bitbake",
}


# ==========================
# CONSTRUIR ALIASES LIMPIOS
# ==========================

TECH_ALIASES = {
    clean_tech_name(k): v
    for k, v in RAW_ALIASES.items()
}


# ==========================
# CATEGORÍAS MEJORADAS
# ==========================

TECH_CATEGORIES = {
    # Lenguajes
    "python": "language",
    "javascript": "language",
    "typescript": "language",
    "java": "language",
    "csharp": "language",
    "cpp": "language",
    "c": "language",
    "rust": "language",
    "go": "language",
    "kotlin": "language",
    "swift": "language",
    "php": "language",
    "ruby": "language",
    "scala": "language",
    "r": "language",
    "matlab": "language",
    "julia": "language",
    "elixir": "language",
    "clojure": "language",
    "haskell": "language",
    "perl": "language",
    "lua": "language",
    "dart": "language",
    "groovy": "language",
    "objectivec": "language",
    "vba": "language",
    "powershell": "language",
    "bash": "language",
    "shell": "language",
    "zsh": "language",
    "html": "language",
    "css": "language",
    "htmlcss": "language",
    "assembly": "language",
    
    # Runtimes
    "nodejs": "runtime",
    "deno": "runtime",
    "bun": "runtime",
    
    # Frameworks
    "react": "framework",
    "vue": "framework",
    "angular": "framework",
    "svelte": "framework",
    "jquery": "framework",
    "nextjs": "framework",
    "gatsby": "framework",
    "tailwind": "framework",
    "django": "framework",
    "flask": "framework",
    "fastapi": "framework",
    "spring": "framework",
    "springboot": "framework",
    "aspnet": "framework",
    "aspnetcore": "framework",
    "laravel": "framework",
    "rails": "framework",
    "express": "framework",
    "nestjs": "framework",
    "astro": "framework",
    "solidjs": "framework",
    "remix": "framework",
    "nuxt": "framework",
    "axum": "framework",
    "blade": "framework",
    
    # Databases
    "postgresql": "database",
    "mysql": "database",
    "mongodb": "database",
    "redis": "database",
    "elasticsearch": "database",
    "cassandra": "database",
    "dynamodb": "database",
    "sqlite": "database",
    "mariadb": "database",
    "oracle": "database",
    "sqlserver": "database",
    "firebase": "database",
    "firestore": "database",
    "redshift": "database",
    "bigquery": "database",
    "snowflake": "database",
    "duckdb": "database",
    
    # Data Engineering
    "polars": "data_engineering",
    "pandas": "data_engineering",
    "numpy": "data_engineering",
    "spark": "data_engineering",
    "hadoop": "data_engineering",
    "kafka": "data_engineering",
    "airflow": "data_engineering",
    "dbt": "data_engineering",
    "databricks": "data_engineering",
    
    # Cloud
    "aws": "cloud",
    "azure": "cloud",
    "gcp": "cloud",
    "alibaba_cloud": "cloud",
    "s3": "cloud",
    "ec2": "cloud",
    "lambda": "cloud",
    "rds": "cloud",
    
    # DevOps
    "docker": "devops",
    "kubernetes": "devops",
    "terraform": "devops",
    "ansible": "devops",
    "jenkins": "devops",
    "githubactions": "devops",
    "gitlabci": "devops",
    "circleci": "devops",
    "prometheus": "devops",
    "grafana": "devops",
    "helm": "devops",
    "nginx": "devops",
    "bicep": "devops",
    
    # AI/ML Technologies
    "tensorflow": "ai_ml",
    "pytorch": "ai_ml",
    "keras": "ai_ml",
    "scikitlearn": "ai_ml",
    "opencv": "ai_ml",
    "huggingface": "ai_ml",
    "langchain": "ai_ml",
    "openai": "ai_ml",
    "gpt": "ai_ml",
    "openai_gpt": "ai_ml",
    "claude": "ai_ml",
    "deepseek": "ai_ml",
    "deepseek_reasoning": "ai_ml",
    "gemini": "ai_ml",
    "github_copilot": "ai_ml",
    "mistral": "ai_ml",
    "llama": "ai_ml",
    "alibaba_qwen": "ai_ml",
    
    # Research Areas
    "machine_learning": "research",
    "deep_learning": "research",
    "nlp": "research",
    "computer_vision": "research",
    "reinforcement_learning": "research",
    "generative_ai": "research",
    "llm": "research",
    "rag": "research",
    "amazon_titan": "research",
    
    # Blockchain
    "blockchain": "emerging",
    "ethereum": "emerging",
    "solidity": "emerging",
    "web3": "emerging",
    "quantum_computing": "emerging",
    
    # Architecture & Integration
    "serverless": "architecture",
    "microservices": "architecture",
    "edge_computing": "architecture",
    "api": "integration",
    "graphql": "integration",
    "rest": "integration",
    
    # Other
    "centreon": "monitoring",
    "antlr": "tooling",
    "apt": "tooling",
    "batch": "tooling",
    "bitbake": "tooling",
}


# ==========================
# TREND TYPES
# ==========================

def get_trend_type(tech: str, scores: dict) -> str:
    """
    Determina el tipo de tendencia de una tecnología.
    
    Args:
        tech: Nombre de la tecnología normalizada
        scores: Diccionario con scores (research_score, github_score, stackoverflow_score)
    
    Returns:
        str: Tipo de tendencia
    """
    research = scores.get('research_score', 0)
    github = scores.get('github_score', 0)
    stackoverflow = scores.get('stackoverflow_score', 0)
    
    # Si todo está bajo, es "emerging"
    if research < 30 and github < 30 and stackoverflow < 30:
        return "Emerging"
    
    # Rising Star: Research alto, GitHub creciendo, SO todavía bajo
    if research > 60 and github > 60 and stackoverflow < 40:
        return "Rising Star"
    
    # Established Leader: Todo alto
    if research > 70 and github > 70 and stackoverflow > 70:
        return "Established Leader"
    
    # Research Driven: Research alto, adopción baja
    if research > 70 and github < 50 and stackoverflow < 40:
        return "Research Driven"
    
    # Community Driven: GitHub alto, SO medio
    if github > 70 and stackoverflow > 40:
        return "Community Driven"
    
    # Industry Standard: SO alto, GitHub medio
    if stackoverflow > 70 and github > 50:
        return "Industry Standard"
    
    # Default
    return "Growing"


# ==========================
# FUNCIONES PÚBLICAS
# ==========================

def normalize_technology(name: str) -> str:
    """
    Normaliza el nombre de una tecnología.
    
    Args:
        name: Nombre original de la tecnología
        
    Returns:
        str: Nombre normalizado o string vacío
    """
    if not name:
        return ""
    
    # Limpiar el nombre
    clean_name = clean_tech_name(name)
    
    # Verificar blacklist
    if clean_name in IGNORE_TECHNOLOGIES:
        return ""
    
    # Buscar en alias
    if clean_name in TECH_ALIASES:
        return TECH_ALIASES[clean_name]
    
    # Buscar coincidencias parciales (con protección contra falsos positivos)
    for alias, canonical in TECH_ALIASES.items():
        # Evitar falsos positivos con alias muy cortos (ej: "c" o "r")
        if len(alias) <= 2:
            if clean_name == alias:
                return canonical
            continue
        
        if alias in clean_name or clean_name in alias:
            return canonical
    
    # Si no hay alias, devolver el nombre limpio
    return clean_name


def get_category(tech: str) -> str:
    """Retorna la categoría de una tecnología normalizada."""
    category = TECH_CATEGORIES.get(tech, "uncategorized")
    # Evitar "other" en dashboard
    if category == "other":
        return "uncategorized"
    return category


# ==========================
# NOMBRES PARA DASHBOARD
# ==========================

METRIC_DISPLAY_NAMES = {
    'future_score': 'Future Score',
    'ranking_score': 'Final Ranking',  # Cambiamos para no mostrar ranking_score directamente
    'stackoverflow_score': 'Developer Adoption',
    'github_score': 'Open Source Momentum',
    'research_score': 'arXiv Research Impact',
    'coverage_score': 'Data Coverage',
}

def get_metric_display_name(metric_key: str) -> str:
    """Retorna el nombre amigable para una métrica."""
    return METRIC_DISPLAY_NAMES.get(metric_key, metric_key.replace('_', ' ').title())


# ==========================
# ICONOS PARA MÉTRICAS
# ==========================

METRIC_ICONS = {
    'future_score': '🎯',
    'ranking_score': '📊',
    'stackoverflow_score': '💻',
    'github_score': '🚀',
    'research_score': '🔬',
    'coverage_score': '📈',
}

def get_metric_icon(metric_key: str) -> str:
    """Retorna el icono para una métrica."""
    return METRIC_ICONS.get(metric_key, '📊')


# ==========================
# CONFIDENCE LEVEL
# ==========================

def get_confidence_level(coverage_score: float) -> str:
    """Retorna el nivel de confianza basado en coverage_score."""
    if coverage_score >= 80:
        return "High"
    elif coverage_score >= 50:
        return "Medium"
    else:
        return "Low"