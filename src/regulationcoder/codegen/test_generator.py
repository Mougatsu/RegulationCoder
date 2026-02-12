"""TestGenerator — generates pytest test functions from rule test cases."""

import logging
import re
import textwrap

from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)


class TestGenerator:
    """Generate pytest test code from Rule test cases.

    This generator does not require an LLM — it deterministically converts
    the structured test cases attached to a Rule into pytest functions.

    Usage:
        generator = TestGenerator()
        test_code = generator.generate(rule)
    """

    def generate(self, rule: Rule) -> str:
        """Generate pytest source code for a Rule's test cases.

        Args:
            rule: A Rule object whose test_cases will be converted to pytest functions.

        Returns:
            A string containing valid pytest Python source code.
        """
        function_name = self._rule_id_to_snake(rule.id)
        module_name = f"evaluate_{function_name}"

        lines: list[str] = []

        # Module docstring
        lines.append(f'"""Auto-generated tests for rule {rule.id}."""')
        lines.append("")
        lines.append("import pytest")
        lines.append("")
        lines.append("")

        # Generate the inline evaluation function reference comment
        lines.append(f"# Tests for: {rule.id}")
        lines.append(f"# Title: {rule.title}")
        lines.append(f"# Requirement: {rule.requirement_id}")
        lines.append("")

        if not rule.test_cases:
            # Generate a placeholder test
            lines.append("")
            lines.append(f"def test_{function_name}_placeholder():")
            lines.append(f'    """Placeholder test — no test cases defined for {rule.id}."""')
            lines.append(f"    pytest.skip('No test cases defined for {rule.id}')")
            lines.append("")
            code = "\n".join(lines)
            logger.info("Generated placeholder test for rule %s (no test cases)", rule.id)
            return code

        # Generate a test function for each test case
        for tc in rule.test_cases:
            test_func_name = self._sanitize_test_name(tc.id, function_name)
            expected = tc.expected_result

            lines.append("")
            lines.append(f"def {test_func_name}():")

            # Docstring
            desc = tc.description.replace('"', '\\"')
            lines.append(f'    """{desc}"""')

            # Input data
            input_repr = repr(tc.input_data)
            lines.append(f"    profile = {input_repr}")
            lines.append("")

            # Call the evaluation function
            lines.append(f"    from regulationcoder.rules.generated import {module_name}")
            lines.append(f"    result = {module_name}(profile)")
            lines.append("")

            # Assertion
            lines.append(f'    assert result == "{expected}", (')
            lines.append(f'        f"Expected \\"{expected}\\" but got \\"{{result}}\\" '
                         f'for {rule.id}"')
            lines.append("    )")
            lines.append("")

        code = "\n".join(lines)
        logger.info(
            "Generated %d test functions for rule %s",
            len(rule.test_cases),
            rule.id,
        )
        return code

    @staticmethod
    def _rule_id_to_snake(rule_id: str) -> str:
        """Convert a rule ID to a snake_case suffix.

        Example: 'RULE-EU-AI-ACT-010-02F-001' -> 'eu_ai_act_010_02f_001'
        """
        suffix = rule_id
        if suffix.upper().startswith("RULE-"):
            suffix = suffix[5:]
        return suffix.replace("-", "_").lower()

    @staticmethod
    def _sanitize_test_name(test_case_id: str, function_name: str) -> str:
        """Create a valid Python test function name from a test case ID.

        Example: 'TC-EU-AI-ACT-010-02F-001-001' -> 'test_eu_ai_act_010_02f_001_001'
        """
        # Replace non-alphanumeric characters with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9]", "_", test_case_id).lower()
        # Ensure it starts with test_
        if not sanitized.startswith("test_"):
            sanitized = f"test_{sanitized}"
        return sanitized
