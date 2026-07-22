"""
Extractor de papers de arXiv.
Simple, limpio, sin conocimiento de tecnologías específicas.
"""

from typing import List, Optional
import time
import xml.etree.ElementTree as ET
import pandas as pd
import requests

from src.config.arxiv_mapping import (
    build_arxiv_queries,
    get_all_technologies
)

BASE_URL = "http://export.arxiv.org/api/query"

PAPER_FIELDS = [
    "id",
    "title",
    "summary",
    "published",
    "updated",
    "authors",
    "categories",
    "pdf_url",
    "primary_category",
    "technology"
]


def _search_arxiv(
    query: str,
    max_results: int = 100,
    start: int = 0
) -> List[dict]:

    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        root = ET.fromstring(response.text)

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }


        papers = []


        for entry in root.findall("atom:entry", ns):

            authors = [
                author.find("atom:name", ns).text
                for author in entry.findall("atom:author", ns)
            ]


            categories = [
                category.attrib.get("term")
                for category in entry.findall("atom:category", ns)
            ]


            pdf_url = None

            for link in entry.findall("atom:link", ns):

                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib.get("href")
                    break


            primary_category = entry.find(
                "arxiv:primary_category",
                ns
            )

            if primary_category is not None:
                primary_category = primary_category.attrib.get("term")


            papers.append({

                "id": entry.findtext(
                    "atom:id",
                    default="",
                    namespaces=ns
                ),

                "title": entry.findtext(
                    "atom:title",
                    default="",
                    namespaces=ns
                ).strip(),

                "summary": entry.findtext(
                    "atom:summary",
                    default="",
                    namespaces=ns
                ).strip(),

                "published": entry.findtext(
                    "atom:published",
                    default="",
                    namespaces=ns
                ),

                "updated": entry.findtext(
                    "atom:updated",
                    default="",
                    namespaces=ns
                ),

                "authors": authors,
                "categories": categories,
                "pdf_url": pdf_url,
                "primary_category": primary_category,

            })


        time.sleep(3)

        return papers


    except Exception as e:

        print(
            f"❌ Error en query '{query}': {e}"
        )

        return []


def extract_arxiv(
    technologies: Optional[List[str]] = None,
    max_papers: int = 500
) -> pd.DataFrame:
    """
    Extrae papers de arXiv para las tecnologías especificadas.

    Args:
        technologies: Lista de tecnologías
        max_papers: Máximo de papers por tecnología

    Returns:
        DataFrame con papers
    """

    if technologies is None:
        technologies = get_all_technologies()

    print(f"🚀 Extrayendo {len(technologies)} tecnologías desde arXiv...")

    all_papers = []

    for i, tech in enumerate(technologies, 1):

        queries = build_arxiv_queries(tech)

        if not queries:
            print(f"⚠️ [{i}/{len(technologies)}] {tech}: sin mapping")
            continue

        print(f"📄 [{i}/{len(technologies)}] {tech}...", end=" ")

        tech_papers = []

        per_query = max(1, max_papers // len(queries))

        for query in queries:

            collected = 0
            start = 0

            while collected < per_query:

                batch = min(
                    100,
                    per_query - collected
                )

                papers = _search_arxiv(
                    query,
                    max_results=batch,
                    start=start
                )

                if not papers:
                    break


                tech_papers.extend(papers)

                collected += len(papers)

                start += batch

        for paper in tech_papers:
            paper["technology"] = tech

        all_papers.extend(tech_papers)

        print(f"✅ {len(tech_papers)} papers")

    if not all_papers:
        print("⚠️ No se obtuvieron papers")
        return pd.DataFrame(columns=PAPER_FIELDS)

    df = pd.DataFrame(all_papers)

    for field in PAPER_FIELDS:
        if field not in df.columns:
            df[field] = None

    df = df[PAPER_FIELDS]

    df["published"] = pd.to_datetime(df["published"])
    df["updated"] = pd.to_datetime(df["updated"])

    print(f"\n✅ Total: {len(df)} papers")

    print("📊 Top tecnologías:")

    for tech, count in df["technology"].value_counts().head(10).items():
        print(f"   {tech}: {count}")

    return df


if __name__ == "__main__":

    test = [
        "Python",
        "React",
        "Docker",
        "openAI GPT (chatbot models)",
        "Meta Llama (all models)"
    ]

    df = extract_arxiv(test, max_papers=5)

    print(df[[
        "technology",
        "title",
        "published"
    ]].head())