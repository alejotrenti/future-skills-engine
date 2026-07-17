from pathlib import Path
import streamlit as st


def _resolve_css_path(css_file: str) -> Path | None:
    """Resolve the CSS file from the local dashboard folder or the current working directory."""
    candidates = [
        Path(__file__).resolve().parent / ".streamlit" / css_file,
        Path(__file__).resolve().parent / css_file,
        Path.cwd() / ".streamlit" / css_file,
        Path.cwd() / css_file,
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def load_css(css_file: str = "app.css") -> None:
    """Load a CSS file from the dashboard .streamlit folder into Streamlit."""
    css_path = _resolve_css_path(css_file)

    if css_path is None:
        return

    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_css_bundle(*css_files: str) -> None:
    """Load multiple CSS files in sequence to keep styles organized by page."""
    css_chunks = []
    for css_file in css_files:
        css_path = _resolve_css_path(css_file)
        if css_path is not None:
            css_chunks.append(css_path.read_text(encoding="utf-8"))

    if css_chunks:
        st.markdown(f"<style>{''.join(css_chunks)}</style>", unsafe_allow_html=True)


def load_all_css() -> None:
    """Backward-compatible wrapper for loading the main dashboard stylesheet."""
    load_css("app.css")
