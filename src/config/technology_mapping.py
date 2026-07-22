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
    "HTML/CSS": "html",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Python": "python",
    "Java": "java",
    "C#": "csharp",
    "C++": "cpp",
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
    "Node.js": "nodejs",
    "NodeJS": "nodejs",
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
    
    # ==========================
    # ALIBABA
    # ==========================
    "Alibaba Cloud": "alibaba_cloud",
    "Alibaba Cloud Qwen": "alibaba_qwen",
    "Alibaba Cloud Qwen models": "alibaba_qwen",
    "Qwen": "alibaba_qwen",
    
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
    "Llama": "llama",
    "LangChain": "langchain",
    "OpenAI": "openai",
    "OpenAI GPT": "openai_gpt",
    "GPT": "gpt",
    "Claude": "claude",
    "Anthropic Claude": "claude",
    "DeepSeek": "deepseek",
    "DeepSeek R": "deepseek_reasoning",
    
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
    # OTROS
    # ==========================
    "Serverless": "serverless",
    "Microservices": "microservices",
    "API": "api",
    "GraphQL": "graphql",
    "REST": "rest",
    "REST API": "rest",
    "Edge Computing": "edge_computing",
    "Quantum Computing": "quantum_computing",
    "Amazon Titan": "amazon_titan",
    "Amazon Titan models": "amazon_titan",
    "Centreon": "centreon",
}


# ==========================
# CONSTRUIR ALIASES LIMPIOS
# ==========================

TECH_ALIASES = {
    clean_tech_name(k): v
    for k, v in RAW_ALIASES.items()
}


# ==========================
# CATEGORÍAS
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
    
    # Frameworks
    "react": "framework",
    "vue": "framework",
    "angular": "framework",
    "svelte": "framework",
    "jquery": "framework",
    "nextjs": "framework",
    "gatsby": "framework",
    "tailwind": "framework",
    "nodejs": "framework",
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
    
    # Cloud & DevOps
    "docker": "devops",
    "kubernetes": "devops",
    "aws": "cloud",
    "azure": "cloud",
    "gcp": "cloud",
    "terraform": "devops",
    "ansible": "devops",
    "jenkins": "devops",
    "githubactions": "devops",
    "gitlabci": "devops",
    "circleci": "devops",
    "s3": "cloud",
    "ec2": "cloud",
    "lambda": "cloud",
    "rds": "cloud",
    "alibaba_cloud": "cloud",
    "alibaba_qwen": "ai_ml",
    
    # AI/ML Technologies
    "tensorflow": "ai_ml",
    "pytorch": "ai_ml",
    "keras": "ai_ml",
    "scikitlearn": "ai_ml",
    "opencv": "ai_ml",
    "huggingface": "ai_ml",
    "llama": "ai_ml",
    "langchain": "ai_ml",
    "openai": "ai_ml",
    
    # Research Areas
    "machine_learning": "research_area",
    "deep_learning": "research_area",
    "nlp": "research_area",
    "computer_vision": "research_area",
    "reinforcement_learning": "research_area",
    "generative_ai": "research_area",
    "llm": "research_area",
    "rag": "research_area",
    "gpt": "research_area",
    "openai_gpt": "research_area",
    "claude": "research_area",
    "deepseek": "research_area",
    "deepseek_reasoning": "research_area",
    "amazon_titan": "research_area",
    
    # Big Data
    "spark": "data",
    "hadoop": "data",
    "kafka": "data",
    "airflow": "data",
    "dbt": "data",
    "databricks": "data",
    
    # Blockchain
    "blockchain": "blockchain",
    "ethereum": "blockchain",
    "solidity": "blockchain",
    "web3": "blockchain",
    
    # Other
    "serverless": "infrastructure",
    "microservices": "architecture",
    "api": "integration",
    "graphql": "integration",
    "rest": "integration",
    "edge_computing": "infrastructure",
    "quantum_computing": "emerging",
    "centreon": "monitoring",
    "antlr": "tools",
    "apt": "tools",
    "assembly": "language",
    "astro": "framework",
    "axum": "framework",
    "batch": "tools",
    "bicep": "devops",
    "bitbake": "tools",
    "blade": "framework",
}


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
    
    # Buscar coincidencias parciales
    for alias, canonical in TECH_ALIASES.items():
        if alias in clean_name or clean_name in alias:
            # Evitar falsos positivos (ej: "aws" en "awslambda")
            if len(alias) > 3 or alias == clean_name:
                return canonical
    
    # Si no hay alias, devolver el nombre limpio
    return clean_name


def get_category(tech: str) -> str:
    """Retorna la categoría de una tecnología normalizada."""
    return TECH_CATEGORIES.get(tech, "other")