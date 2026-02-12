"""Custom exceptions for RegulationCoder."""


class RegulationCoderError(Exception):
    """Base exception for all RegulationCoder errors."""


class IngestionError(RegulationCoderError):
    """Error during document ingestion."""


class ParsingError(RegulationCoderError):
    """Error during clause parsing."""


class ExtractionError(RegulationCoderError):
    """Error during requirement extraction."""


class FormalizationError(RegulationCoderError):
    """Error during rule formalization."""


class CodeGenerationError(RegulationCoderError):
    """Error during code generation."""


class JudgeError(RegulationCoderError):
    """Error during judge gate evaluation."""


class JudgeBlockError(JudgeError):
    """Judge gate blocked the item."""

    def __init__(self, stage: str, target_ids: list[str], reason: str):
        self.stage = stage
        self.target_ids = target_ids
        self.reason = reason
        super().__init__(f"Judge blocked at {stage} for {target_ids}: {reason}")


class JudgeReviseError(JudgeError):
    """Judge gate requested revision."""

    def __init__(self, stage: str, target_ids: list[str], fixes: list[str]):
        self.stage = stage
        self.target_ids = target_ids
        self.fixes = fixes
        super().__init__(f"Judge requested revision at {stage} for {target_ids}")


class DiffError(RegulationCoderError):
    """Error during diff analysis."""


class ExportError(RegulationCoderError):
    """Error during report export."""


class ConfigError(RegulationCoderError):
    """Configuration error."""
