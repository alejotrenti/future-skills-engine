"""
Configuración de búsquedas para arXiv.
Cada tecnología puede tener una o múltiples queries para maximizar la cobertura.
"""

from typing import List

ARXIV_MAPPING: dict[str, str | list[str]] = {
    # ========== LENGUAJES DE PROGRAMACIÓN ==========
    "Python": [
        '"Python programming"',
        '"Python language"',
        '"Python code"',
        '"Python software"'
    ],
    
    "JavaScript": [
        '"JavaScript programming"',
        '"JavaScript language"'
    ],
    
    "TypeScript": [
        '"TypeScript programming"',
        '"TypeScript language"'
    ],
    
    "Java": [
        '"Java programming"',
        '"Java language"',
        '"Java framework"'
    ],
    
    "Rust": [
        '"Rust programming"',
        '"Rust language"',
        '"Rust compiler"'
    ],
    
    "Go": [
        '"Go programming"',
        '"Golang"',
        '"Go language"'
    ],
    
    "C#": [
        '"C sharp"',
        '"C# programming"',
    ],
    
    "C++": [
        '"C plus plus"',
        '"C++ programming"',
        '"C++ language"'
    ],
    
    # ========== FRAMEWORKS ==========
    "React": [
        '"React.js"',
        '"ReactJS"',
        '"React framework"',
        '"React library"'
    ],
    
    "Vue.js": [
        '"Vue.js"',
        '"VueJS"',
        '"Vue framework"'
    ],
    
    "Angular": [
        '"Angular framework"',
        '"AngularJS"',
        '"Angular web framework"'
    ],
    
    "Django": [
        '"Django"',
        '"Django framework"',
        '"Django Python"'
    ],
    
    "FastAPI": [
        '"FastAPI"',
        '"Fast API"',
        '"FastAPI framework"'
    ],
    
    # ========== INFRAESTRUCTURA ==========
    "Docker": [
        '"Docker"',
        '"Docker container"',
        '"Docker orchestration"'
    ],
    
    "Kubernetes": [
        '"Kubernetes"',
        '"k8s"',
        '"Kubernetes orchestration"'
    ],
    
    # ========== BASES DE DATOS ==========
    "PostgreSQL": [
        '"PostgreSQL"',
        '"Postgres"',
        '"PostgreSQL database"'
    ],
    
    "MongoDB": [
        '"MongoDB"',
        '"Mongo"',
        '"MongoDB database"'
    ],
    
    # ========== MODELOS DE IA (específicos) ==========
    "openAI GPT (chatbot models)": [
        '"GPT-3"',
        '"GPT-4"',
        '"GPT-4o"',
        '"ChatGPT"',
        '"large language model"',
        '"generative pre-trained transformer"'
    ],
    
    "Anthropic: Claude Sonnet": [
        '"Claude AI"',
        '"Anthropic Claude"',
        '"Claude Sonnet"'
    ],
    
    "Gemini (Flash general purpose models)": [
        '"Gemini AI"',
        '"Google Gemini"',
        '"Gemini Flash"'
    ],
    
    "Gemini (Pro Reasoning models)": [
        '"Gemini Pro"',
        '"Gemini reasoning"',
        '"Google Gemini Pro"'
    ],
    
    "Meta Llama (all models)": [
        '"Meta Llama"',
        '"LLaMA model"',
        '"Llama large language model"'
    ],
    
    "DeepSeek (R- Reasoning models)": [
        '"DeepSeek"',
        '"DeepSeek R1"',
        '"DeepSeek reasoning"'
    ],
    
    "DeepSeek (V- General purpose models)": [
        '"DeepSeek V3"',
        '"DeepSeek"',
        '"DeepSeek model"'
    ],
    
    "Mistral AI models": [
        '"Mistral"',
        '"Mistral AI"',
        '"Mistral model"'
    ],
    
    "Alibaba Cloud Qwen models": [
        '"Qwen"',
        '"Alibaba Qwen"',
        '"Qwen model"'
    ],
}


def normalize_queries(queries: str | list[str]) -> list[str]:
    """
    Normaliza las queries para asegurar que siempre devuelva una lista.
    
    Args:
        queries: String o lista de strings
        
    Returns:
        Lista de strings con las queries normalizadas
    """
    if isinstance(queries, str):
        return [queries]
    return queries


def build_arxiv_queries(technology: str) -> list[str]:
    """
    Construye las queries de búsqueda para arXiv para una tecnología dada.
    
    Args:
        technology: Nombre de la tecnología a buscar
        
    Returns:
        Lista de queries formateadas para la API de arXiv
        
    Example:
        >>> build_arxiv_queries("React")
        ['all:React', 'all:"React.js"', 'all:"ReactJS"']
    """
    raw_queries = ARXIV_MAPPING.get(technology, [])
    
    if not raw_queries:
        return []
    
    # Normalizar a lista
    queries_list = normalize_queries(raw_queries)
    
    # Formatear para búsqueda en arXiv (campo all:)
    return [f"all:{query}" for query in queries_list]


def get_all_technologies() -> list[str]:
    """
    Obtiene todas las tecnologías disponibles en el mapping.
    
    Returns:
        Lista de nombres de tecnologías
    """
    return list(ARXIV_MAPPING.keys())