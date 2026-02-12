"""Unit tests for the parser module."""

import pytest

from regulationcoder.models.clause import Clause
from regulationcoder.models.citation import Citation


class TestClauseSegmenter:
    def test_segment_article(self):
        from regulationcoder.parser.segmenter import ClauseSegmenter

        segmenter = ClauseSegmenter()
        text = """Article 10
Data and data governance

1. High-risk AI systems which make use of techniques involving the training of AI models with data shall be developed on the basis of training, validation and testing data sets that meet the quality criteria referred to in paragraphs 2 to 5.

2. Training, validation and testing data sets shall be subject to data governance and management practices appropriate for the intended purpose of the AI system. Those practices shall concern in particular:

(a) the relevant design choices;

(b) data collection processes and the origin of data;

(c) the relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation;
"""
        clauses = segmenter.segment(text, "eu-ai-act", "2024-1689-oj")
        assert len(clauses) > 0
        assert all(isinstance(c, Clause) for c in clauses)
        assert all(c.regulation_id == "eu-ai-act" for c in clauses)
        # Should have article-level, paragraph-level, and subsection-level clauses
        article_level = [c for c in clauses if c.paragraph_number is None]
        para_level = [c for c in clauses if c.paragraph_number and not c.subsection_letter]
        sub_level = [c for c in clauses if c.subsection_letter]
        assert len(para_level) >= 2
        assert len(sub_level) >= 2

    def test_deterministic_ids(self):
        from regulationcoder.parser.segmenter import ClauseSegmenter

        segmenter = ClauseSegmenter()
        text = "Article 9\nRisk management\n\n1. A risk management system shall be established."
        clauses = segmenter.segment(text, "eu-ai-act", "v1")
        # Run again
        clauses2 = segmenter.segment(text, "eu-ai-act", "v1")
        assert [c.id for c in clauses] == [c.id for c in clauses2]


class TestCitationExtractor:
    def test_extract_article_refs(self):
        from regulationcoder.parser.citation_extractor import CitationExtractor

        extractor = CitationExtractor()
        text = "as referred to in Article 6(2) and Article 10(3)"
        citations = extractor.extract(text, "eu-ai-act-v1/art9/para1")
        assert len(citations) >= 1
        assert any("Article 6" in c.article_ref or "Article 10" in c.article_ref for c in citations)


class TestDocumentTreeBuilder:
    def test_build_tree(self):
        from regulationcoder.parser.tree_builder import DocumentTreeBuilder

        clauses = [
            Clause(
                id="reg/art10",
                regulation_id="reg",
                document_version="v1",
                article_number=10,
                text="Article 10 header",
            ),
            Clause(
                id="reg/art10/para1",
                regulation_id="reg",
                document_version="v1",
                article_number=10,
                paragraph_number=1,
                text="Paragraph 1",
                parent_clause_id="reg/art10",
            ),
            Clause(
                id="reg/art10/para1/sub-a",
                regulation_id="reg",
                document_version="v1",
                article_number=10,
                paragraph_number=1,
                subsection_letter="a",
                text="Subsection a",
                parent_clause_id="reg/art10/para1",
            ),
        ]
        builder = DocumentTreeBuilder()
        root = builder.build(clauses)
        # Virtual root holds article-level nodes as children
        assert len(root.children) == 1
        assert len(root.children[0].children) == 1
        assert len(root.children[0].children[0].children) == 1
