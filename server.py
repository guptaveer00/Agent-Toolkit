"""Expose HW6 StatsHelper textbook retrieval as a local stdio MCP tool."""

import argparse
from pathlib import Path

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


def build_server(stats_helper: Path) -> FastMCP:
    index = stats_helper / "chroma_store"
    if not (index / "chroma.sqlite3").is_file():
        raise SystemExit(f"No StatsHelper Chroma index at {index}")

    embedding = ONNXMiniLM_L6_V2()
    embedding.DOWNLOAD_PATH = stats_helper / ".model_cache" / embedding.MODEL_NAME
    client = chromadb.PersistentClient(
        path=str(index), settings=Settings(anonymized_telemetry=False)
    )
    collection = client.get_collection("study_v2", embedding_function=embedding)
    server = FastMCP("stats-helper")

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    def search_stats_passages(question: str) -> list[dict]:
        """Find up to five textbook passages in the local HW6 index for a statistics question.

        Ask in plain language. Results include passage text, PDF page, and cosine
        distance in rank order. Lower distances indicate closer matches. Read the
        passage before relying on it. Personal notes are excluded.
        """
        question = question.strip()
        if not question:
            raise ValueError("Provide a non-empty statistics question.")
        result = collection.query(
            query_texts=[question],
            n_results=5,
            where={"kind": "textbook"},
            include=["documents", "metadatas", "distances"],
        )
        return [
            {"id": id_, "pdf_page": metadata["pdf_page"], "text": passage,
             "cosine_distance": distance}
            for id_, passage, metadata, distance in zip(
                result["ids"][0], result["documents"][0],
                result["metadatas"][0], result["distances"][0], strict=True,
            )
        ]

    return server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stats_helper", type=Path, help="Path to a local StatsHelper index and model cache")
    args = parser.parse_args()
    build_server(args.stats_helper.expanduser().resolve()).run(transport="stdio")
