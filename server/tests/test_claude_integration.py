"""
test_claude_integration.py — Tests for the Claude / roadmap service.

The real Claude API is NOT called in the unit test suite.  The actual
API-key test should only be run locally with a valid key (marked with
``@pytest.mark.integration`` and excluded from CI via pyproject.toml config).

Coverage targets
----------------
* generate_roadmap_with_claude (placeholder)  → structure validation
* services module error paths (future: real integration against live API)
"""

from __future__ import annotations

import pytest

from extraction.services import generate_roadmap_with_claude

# ══════════════════════════════════════════════════════════════════════════════
# Placeholder / unit tests (always run in CI)
# ══════════════════════════════════════════════════════════════════════════════


class TestGenerateRoadmapDummy:
    """Validate the placeholder roadmap function returns the expected structure."""

    @pytest.mark.asyncio
    async def test_returns_dict_with_roadmap_key(self) -> None:
        """Result must be a dict containing a 'roadmap' list."""
        result = await generate_roadmap_with_claude(
            missing_skills=["python"], jd_text="Need Python dev"
        )
        assert isinstance(result, dict)
        assert "roadmap" in result

    @pytest.mark.asyncio
    async def test_returns_non_empty_roadmap_list(self) -> None:
        """The roadmap list must have at least one item."""
        result = await generate_roadmap_with_claude(
            missing_skills=["python"], jd_text="Need Python dev"
        )
        assert isinstance(result["roadmap"], list)
        assert len(result["roadmap"]) > 0

    @pytest.mark.asyncio
    async def test_roadmap_items_have_required_keys(self) -> None:
        """Each roadmap item must contain 'timeline', 'focus', and 'resources'."""
        result = await generate_roadmap_with_claude(missing_skills=["python"])
        for item in result["roadmap"]:
            assert "timeline" in item, f"Missing 'timeline' in {item}"
            assert "focus" in item, f"Missing 'focus' in {item}"
            assert "resources" in item, f"Missing 'resources' in {item}"

    @pytest.mark.asyncio
    async def test_resources_is_a_list(self) -> None:
        """The 'resources' field within each roadmap item must be a list."""
        result = await generate_roadmap_with_claude()
        for item in result["roadmap"]:
            assert isinstance(item["resources"], list)

    @pytest.mark.asyncio
    async def test_returns_message_key(self) -> None:
        """Result dict must also contain a 'message' string."""
        result = await generate_roadmap_with_claude()
        assert "message" in result
        assert isinstance(result["message"], str)

    @pytest.mark.asyncio
    async def test_accepts_arbitrary_kwargs(self) -> None:
        """The function should accept any keyword arguments without raising."""
        result = await generate_roadmap_with_claude(
            missing_skills=["react"],
            jd_text="Need React dev",
            extra_param="ignored",
        )
        assert "roadmap" in result

    @pytest.mark.asyncio
    async def test_no_args_does_not_raise(self) -> None:
        """Calling without arguments should be safe."""
        result = await generate_roadmap_with_claude()
        assert isinstance(result, dict)


# ══════════════════════════════════════════════════════════════════════════════
# Integration test — excluded from normal CI runs
# Mark this test with @pytest.mark.integration and exclude it in pyproject.toml:
#   [tool.pytest.ini_options]
#   addopts = "-m 'not integration'"
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.integration
@pytest.mark.asyncio
async def test_anthropic_api_key_is_valid_live() -> None:
    """
    Live integration test: verify the ANTHROPIC_API_KEY is set and accepted
    by the Claude API.

    SKIP in CI — run locally only:
        pytest -m integration server/tests/test_claude_integration.py
    """
    from anthropic import AsyncAnthropic, AuthenticationError

    from core.config import settings

    assert settings.anthropic_api_key, "ANTHROPIC_API_KEY is not configured"

    api_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    try:
        response = await api_client.messages.create(
            max_tokens=10,
            messages=[{"role": "user", "content": "Reply with 'pong'."}],
            model="claude-3-haiku-20240307",
        )
        assert response.content is not None
        assert len(response.content) > 0
    except AuthenticationError:
        pytest.fail("ANTHROPIC_API_KEY is invalid.")
    except Exception as exc:
        pytest.fail(f"Unexpected API error: {exc}")
