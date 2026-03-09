"""
Generates an ER diagram of all SQLAlchemy models as erd.png and erd.svg.

Requirements:
    uv add graphviz            # Python package
    winget install graphviz    # or: https://graphviz.org/download/

Usage:
    uv run python visualize_models.py
"""

import os
import sys

# Allow imports from the backend root without installing the package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Provide a dummy DATABASE_URL so pydantic-settings doesn't error before we
# even connect — the visualizer only reads metadata, it never opens a connection.
os.environ.setdefault("DATABASE_URL", "postgresql://localhost/placeholder")

try:
    from graphviz import Digraph
except ImportError:
    print("ERROR: graphviz not installed.\n  Run: uv add graphviz")
    sys.exit(1)

from core.database import Base
import models  # noqa: F401 — registers all models with Base

# ── Colour palette ────────────────────────────────────────────────────────────
HEADER_BG = "#2563EB"  # blue
HEADER_FG = "white"
PK_BG = "#DBEAFE"  # light blue
FK_BG = "#FEF9C3"  # light yellow
COL_BG = "#F9FAFB"  # near-white
BORDER = "#D1D5DB"  # light grey


def _type_label(col_type) -> str:
    """Return a short, readable type string."""
    s = str(col_type)
    # Trim long precision specs like NUMERIC(18, 2) → NUMERIC
    if "(" in s:
        s = s[: s.index("(")]
    return s.upper()


def _col_row(col) -> str:
    is_pk = col.primary_key
    is_fk = bool(col.foreign_keys)
    nullable = col.nullable and not is_pk

    bg = PK_BG if is_pk else (FK_BG if is_fk else COL_BG)
    tag = " <B>PK</B>" if is_pk else (" <I>FK</I>" if is_fk else "")
    null_marker = " <FONT COLOR='#9CA3AF'>?</FONT>" if nullable else ""
    type_str = _type_label(col.type)

    return (
        f"<TR>"
        f'<TD ALIGN="LEFT" BGCOLOR="{bg}" PORT="{col.name}">'
        f"  {col.name}{tag}{null_marker}"
        f"</TD>"
        f'<TD ALIGN="LEFT" BGCOLOR="{bg}">'
        f'  <FONT COLOR="#6B7280">{type_str}</FONT>'
        f"</TD>"
        f"</TR>"
    )


def _table_node(table) -> str:
    rows = "\n".join(_col_row(c) for c in table.columns)
    return (
        f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
        f'CELLPADDING="4" COLOR="{BORDER}">'
        f"<TR>"
        f'<TD COLSPAN="2" BGCOLOR="{HEADER_BG}" ALIGN="CENTER">'
        f'<FONT COLOR="{HEADER_FG}"><B>{table.name}</B></FONT>'
        f"</TD>"
        f"</TR>"
        f"{rows}"
        f"</TABLE>>"
    )


def build_diagram() -> Digraph:
    dot = Digraph(
        name="Princeton Trading — ER Diagram",
        graph_attr={
            "rankdir": "LR",
            "splines": "ortho",
            "nodesep": "0.6",
            "ranksep": "1.2",
            "bgcolor": "white",
            "fontname": "Helvetica",
            "label": "Princeton Trading — Entity Relationship Diagram",
            "labelloc": "t",
            "fontsize": "16",
        },
        node_attr={"shape": "none", "fontname": "Helvetica", "fontsize": "11"},
        edge_attr={"fontsize": "9", "fontname": "Helvetica", "color": "#6B7280"},
    )

    for table in Base.metadata.sorted_tables:
        dot.node(table.name, label=_table_node(table))

    # One directed edge per FK column: child_table:col → parent_table:col
    seen = set()
    for table in Base.metadata.sorted_tables:
        for col in table.columns:
            for fk in col.foreign_keys:
                parent_table = fk.column.table.name
                parent_col = fk.column.name
                edge_key = (table.name, col.name, parent_table, parent_col)
                if edge_key in seen:
                    continue
                seen.add(edge_key)
                dot.edge(
                    f"{table.name}:{col.name}",
                    f"{parent_table}:{parent_col}",
                    arrowhead="crow",
                    arrowtail="none",
                    dir="both",
                )

    return dot


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "erd")

    diagram = build_diagram()

    diagram.render(output_path, format="png", cleanup=True)
    diagram.render(output_path, format="svg", cleanup=True)

    print(f"Saved:\n  {output_path}.png\n  {output_path}.svg")
