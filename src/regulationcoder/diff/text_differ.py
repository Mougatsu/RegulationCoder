"""TextDiffer — clause-level diff using difflib for structural comparison."""

import difflib
import logging

from regulationcoder.models.clause import Clause
from regulationcoder.models.diff import ChangeType, ClauseChange

logger = logging.getLogger(__name__)


class TextDiffer:
    """Compare two lists of clauses and produce a list of ClauseChange objects.

    Uses difflib.SequenceMatcher to identify added, deleted, modified,
    and unchanged clauses between two regulation versions.
    """

    def diff(
        self, old_clauses: list[Clause], new_clauses: list[Clause]
    ) -> list[ClauseChange]:
        """Diff two ordered lists of clauses and return a list of changes.

        Matching is performed by clause ID.  When a clause ID appears in both
        versions the texts are compared to decide between MODIFIED and
        UNCHANGED.  IDs present only in *old* are DELETED; only in *new* are
        ADDED.
        """
        old_by_id: dict[str, Clause] = {c.id: c for c in old_clauses}
        new_by_id: dict[str, Clause] = {c.id: c for c in new_clauses}

        old_ids = list(old_by_id.keys())
        new_ids = list(new_by_id.keys())

        changes: list[ClauseChange] = []

        # Use SequenceMatcher on the ordered ID lists so we can detect
        # positional moves as well as content changes.
        matcher = difflib.SequenceMatcher(None, old_ids, new_ids)

        processed_old: set[str] = set()
        processed_new: set[str] = set()

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                # IDs match positionally — compare text
                for old_id, new_id in zip(old_ids[i1:i2], new_ids[j1:j2]):
                    processed_old.add(old_id)
                    processed_new.add(new_id)
                    changes.append(
                        self._compare_texts(old_by_id[old_id], new_by_id[new_id])
                    )
            elif tag == "replace":
                # IDs differ positionally — try to pair by ID first
                old_slice = old_ids[i1:i2]
                new_slice = new_ids[j1:j2]
                paired = self._pair_by_id(old_slice, new_slice, old_by_id, new_by_id)

                for old_id, new_id in paired["matched"]:
                    processed_old.add(old_id)
                    processed_new.add(new_id)
                    changes.append(
                        self._compare_texts(old_by_id[old_id], new_by_id[new_id])
                    )
                for cid in paired["deleted"]:
                    processed_old.add(cid)
                    changes.append(
                        ClauseChange(
                            clause_id=cid,
                            change_type=ChangeType.DELETED,
                            old_text=old_by_id[cid].text,
                            new_text="",
                            diff_summary=f"Clause {cid} was deleted.",
                        )
                    )
                for cid in paired["added"]:
                    processed_new.add(cid)
                    changes.append(
                        ClauseChange(
                            clause_id=cid,
                            change_type=ChangeType.ADDED,
                            old_text="",
                            new_text=new_by_id[cid].text,
                            diff_summary=f"Clause {cid} was added.",
                        )
                    )
            elif tag == "delete":
                for cid in old_ids[i1:i2]:
                    processed_old.add(cid)
                    changes.append(
                        ClauseChange(
                            clause_id=cid,
                            change_type=ChangeType.DELETED,
                            old_text=old_by_id[cid].text,
                            new_text="",
                            diff_summary=f"Clause {cid} was deleted.",
                        )
                    )
            elif tag == "insert":
                for cid in new_ids[j1:j2]:
                    processed_new.add(cid)
                    changes.append(
                        ClauseChange(
                            clause_id=cid,
                            change_type=ChangeType.ADDED,
                            old_text="",
                            new_text=new_by_id[cid].text,
                            diff_summary=f"Clause {cid} was added.",
                        )
                    )

        # Safety net: capture any IDs that slipped through
        for cid in set(old_by_id) - processed_old:
            changes.append(
                ClauseChange(
                    clause_id=cid,
                    change_type=ChangeType.DELETED,
                    old_text=old_by_id[cid].text,
                    new_text="",
                    diff_summary=f"Clause {cid} was deleted.",
                )
            )
        for cid in set(new_by_id) - processed_new:
            changes.append(
                ClauseChange(
                    clause_id=cid,
                    change_type=ChangeType.ADDED,
                    old_text="",
                    new_text=new_by_id[cid].text,
                    diff_summary=f"Clause {cid} was added.",
                )
            )

        logger.info(
            "TextDiffer: %d changes (%d added, %d deleted, %d modified, %d unchanged)",
            len(changes),
            sum(1 for c in changes if c.change_type == ChangeType.ADDED),
            sum(1 for c in changes if c.change_type == ChangeType.DELETED),
            sum(1 for c in changes if c.change_type == ChangeType.MODIFIED),
            sum(1 for c in changes if c.change_type == ChangeType.UNCHANGED),
        )
        return changes

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compare_texts(old_clause: Clause, new_clause: Clause) -> ClauseChange:
        """Compare two clause texts and return a ClauseChange."""
        if old_clause.text.strip() == new_clause.text.strip():
            return ClauseChange(
                clause_id=old_clause.id,
                change_type=ChangeType.UNCHANGED,
                old_text=old_clause.text,
                new_text=new_clause.text,
                diff_summary="No change.",
            )

        # Build a human-readable unified diff summary
        diff_lines = list(
            difflib.unified_diff(
                old_clause.text.splitlines(keepends=True),
                new_clause.text.splitlines(keepends=True),
                fromfile="old",
                tofile="new",
                lineterm="",
            )
        )
        summary = "\n".join(diff_lines) if diff_lines else "Text modified."

        return ClauseChange(
            clause_id=old_clause.id,
            change_type=ChangeType.MODIFIED,
            old_text=old_clause.text,
            new_text=new_clause.text,
            diff_summary=summary,
        )

    @staticmethod
    def _pair_by_id(
        old_ids: list[str],
        new_ids: list[str],
        old_by_id: dict[str, Clause],
        new_by_id: dict[str, Clause],
    ) -> dict[str, list]:
        """Pair clauses across a replace block by matching IDs."""
        old_set = set(old_ids)
        new_set = set(new_ids)
        common = old_set & new_set
        return {
            "matched": [(cid, cid) for cid in common],
            "deleted": [cid for cid in old_ids if cid not in common],
            "added": [cid for cid in new_ids if cid not in common],
        }
