"""Build a hierarchical document tree from a flat list of clauses.

The :class:`ClauseSegmenter` produces a flat ``list[Clause]`` where each
clause carries a ``parent_clause_id`` field.  This module reconstructs the
tree so that articles contain their paragraphs, paragraphs contain their
subsections, and so on.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from regulationcoder.core.exceptions import ParsingError
from regulationcoder.models.clause import Clause

logger = logging.getLogger(__name__)


@dataclass
class DocumentNode:
    """A single node in the regulation document tree.

    Attributes
    ----------
    clause:
        The :class:`Clause` data for this node.
    children:
        Ordered list of child nodes (paragraphs under an article,
        subsections under a paragraph, etc.).
    parent:
        Reference to the parent node, or ``None`` for root-level articles.
    """

    clause: Clause
    children: list[DocumentNode] = field(default_factory=list)
    parent: DocumentNode | None = field(default=None, repr=False)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    @property
    def id(self) -> str:
        """Shortcut for the clause ID."""
        return self.clause.id

    @property
    def is_leaf(self) -> bool:
        """``True`` if this node has no children."""
        return len(self.children) == 0

    @property
    def depth(self) -> int:
        """How deep this node is in the tree (root = 0)."""
        level = 0
        node = self.parent
        while node is not None:
            level += 1
            node = node.parent
        return level

    def walk(self) -> list[DocumentNode]:
        """Return all nodes in this subtree in depth-first pre-order."""
        result: list[DocumentNode] = [self]
        for child in self.children:
            result.extend(child.walk())
        return result

    def find(self, clause_id: str) -> DocumentNode | None:
        """Search this subtree for a node with the given *clause_id*."""
        if self.clause.id == clause_id:
            return self
        for child in self.children:
            found = child.find(clause_id)
            if found is not None:
                return found
        return None

    def __str__(self) -> str:
        indent = "  " * self.depth
        line = f"{indent}{self.clause.id}"
        parts = [line]
        for child in self.children:
            parts.append(str(child))
        return "\n".join(parts)


class DocumentTreeBuilder:
    """Reconstruct the document tree from a flat list of :class:`Clause` objects.

    Clauses reference their parent through the ``parent_clause_id`` field.
    Clauses with ``parent_clause_id is None`` are treated as root nodes
    (typically article-level clauses).
    """

    def build(self, clauses: list[Clause]) -> DocumentNode:
        """Build a tree and return a virtual root node containing all articles.

        Parameters
        ----------
        clauses:
            Flat list of clauses as produced by :class:`ClauseSegmenter`.
            The list order does not matter; the builder indexes by ID.

        Returns
        -------
        DocumentNode
            A virtual root node whose ``children`` are the top-level
            article nodes.  The root's own ``clause`` is a synthetic
            placeholder.

        Raises
        ------
        ParsingError
            If the clause list is empty.
        """
        if not clauses:
            raise ParsingError("Cannot build tree from an empty clause list")

        # Index clauses by ID for O(1) lookup.
        node_map: dict[str, DocumentNode] = {}
        for clause in clauses:
            node_map[clause.id] = DocumentNode(clause=clause)

        # Wire up parent ↔ child relationships.
        roots: list[DocumentNode] = []

        for clause in clauses:
            node = node_map[clause.id]

            if clause.parent_clause_id is None:
                roots.append(node)
            else:
                parent_node = node_map.get(clause.parent_clause_id)
                if parent_node is None:
                    # Orphan clause — parent ID referenced but not present.
                    logger.warning(
                        "Clause %s references missing parent %s; treating as root",
                        clause.id,
                        clause.parent_clause_id,
                    )
                    roots.append(node)
                else:
                    node.parent = parent_node
                    parent_node.children.append(node)

        # Sort roots by article number for deterministic output.
        roots.sort(key=lambda n: n.clause.article_number)

        # Sort children within each node by paragraph number then subsection.
        for node in node_map.values():
            node.children.sort(
                key=lambda n: (
                    n.clause.paragraph_number or 0,
                    n.clause.subsection_letter or "",
                )
            )

        # Create a virtual root that holds all article-level nodes.
        virtual_root_clause = Clause(
            id="root",
            regulation_id=clauses[0].regulation_id if clauses else "",
            document_version=clauses[0].document_version if clauses else "",
            article_number=0,
            text="(document root)",
        )
        virtual_root = DocumentNode(clause=virtual_root_clause, children=roots)

        # Set parent on roots to point to the virtual root.
        for root_node in roots:
            root_node.parent = virtual_root

        total_nodes = sum(1 for _ in virtual_root.walk()) - 1  # exclude virtual root
        logger.info(
            "Built document tree: %d root article(s), %d total node(s)",
            len(roots),
            total_nodes,
        )

        return virtual_root
