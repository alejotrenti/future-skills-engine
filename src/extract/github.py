"""
Extractor de datos de GitHub.
Simple, limpio, sin conocimiento de tecnologías específicas.
"""
import os
import time
from typing import List, Optional
import requests
import pandas as pd
from dotenv import load_dotenv

from src.config.github_mapping import build_github_queries, get_all_technologies

load_dotenv()

BASE_URL = "https://api.github.com/search/repositories"
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
} if TOKEN else {
    "Accept": "application/vnd.github+json"
}

REPO_FIELDS = [
    "id",
    "name",
    "full_name",
    "html_url",
    "description",
    "language",
    "stargazers_count",
    "forks_count",
    "watchers_count",
    "open_issues_count",
    "created_at",
    "updated_at",
    "pushed_at",
    "topics",
    "owner.login",
    "license.name",
    "technology"
]


def _search_github(query: str, max_results: int = 100, sort: str = "stars") -> List[dict]:
    """
    Busca repositorios en GitHub.
    
    Args:
        query: Query formateada (language:Python, topic:react, etc)
        max_results: Máximo de repositorios
        sort: Criterio de ordenamiento (stars, updated, etc)
    """
    if not TOKEN:
        raise ValueError(
            "GITHUB_TOKEN no encontrado. Configuralo en el archivo .env"
        )
        
    all_repos = []
    page = 1
    per_page = 30
    
    while len(all_repos) < max_results:
        params = {
            "q": query,
            "per_page": min(per_page, max_results - len(all_repos)),
            "page": page,
            "sort": sort
        }
        
        try:
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            
            # Rate limiting
            if response.status_code == 403:
                remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
                if remaining == 0:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    wait_time = reset_time - time.time()
                    if wait_time > 0:
                        print(f"⏳ Esperando {wait_time:.0f}s...")
                        time.sleep(wait_time + 1)
                    continue
            
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            if not items:
                break
                
            all_repos.extend(items)
            
            if len(items) < per_page:
                break
                
            page += 1
            time.sleep(0.3)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en query '{query}': {e}")
            break
    
    return all_repos


def extract_github(
    technologies: Optional[List[str]] = None,
    max_repos: int = 100,
    sort: str = "stars"
) -> pd.DataFrame:
    """
    Extrae repositorios de GitHub para las tecnologías especificadas.
    
    Args:
        technologies: Lista de tecnologías (todas si None)
        max_repos: Máximo de repositorios por tecnología
        sort: Criterio de ordenamiento (stars, updated, etc)
        
    Returns:
        DataFrame con repositorios
    """
    if technologies is None:
        technologies = get_all_technologies()
    
    print(f"🚀 Extrayendo {len(technologies)} tecnologías de GitHub...")
    
    all_repos = []
    
    for i, tech in enumerate(technologies, 1):
        queries = build_github_queries(tech)
        
        if not queries:
            print(f"⚠️  [{i}/{len(technologies)}] {tech}: sin mapping")
            continue
        
        print(f"📦 [{i}/{len(technologies)}] {tech}...", end=" ")
        
        tech_repos = []
        # Distribuir max_repos entre las queries (para HTML/CSS)
        per_query = max(1, max_repos // len(queries))
        
        for query in queries:
            repos = _search_github(query, per_query, sort)
            tech_repos.extend(repos)
        
        # Marcar cada repositorio con su tecnología
        for repo in tech_repos:
            repo["technology"] = tech
        
        all_repos.extend(tech_repos)
        print(f"✅ {len(tech_repos)} repositorios")
    
    if not all_repos:
        print("⚠️  No se obtuvieron repositorios")
        return pd.DataFrame(columns=REPO_FIELDS)
    
    # Convertir a DataFrame
    df = pd.json_normalize(all_repos)
    
    # Asegurar que todos los campos existan
    for field in REPO_FIELDS:
        if field not in df.columns:
            df[field] = None
    
    df = df[REPO_FIELDS]
    
    # Limpiar y tipificar datos
    numeric_cols = ["stargazers_count", "forks_count", "watchers_count", "open_issues_count"]
    for col in numeric_cols:
        df[col] = df[col].fillna(0).astype(int)
    
    date_cols = ["created_at", "updated_at", "pushed_at"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    
    print(f"\n✅ Total: {len(df)} repositorios")
    print("📊 Top tecnologías:")
    for tech, count in df["technology"].value_counts().head(10).items():
        print(f"   {tech}: {count}")
    
    return df


if __name__ == "__main__":
    # Test rápido
    test = ["Python", "React", "Docker", "HTML/CSS", "openAI GPT (chatbot models)"]
    df = extract_github(test, max_repos=5)
    print("\n🎯 Muestra:")
    print(df[["technology", "name", "html_url", "stargazers_count"]].head(10))
    
