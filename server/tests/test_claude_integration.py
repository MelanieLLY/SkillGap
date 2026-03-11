import pytest
from anthropic import AsyncAnthropic, AuthenticationError
from server.core.config import settings
from server.extraction.services import generate_roadmap_with_claude

@pytest.mark.asyncio
async def test_anthropic_api_key_validity():
    """
    Integration test to verify that the Anthropic API key is valid an can communicate with Claude.
    This test will fail if the key is not set or invalid.
    """
    # Ensure the key is not empty
    assert settings.anthropic_api_key, "ANTHROPIC_API_KEY is not set in the environment"

    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    
    try:
        response = await client.messages.create(
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, this is a test ping. Please reply with 'pong'."
                }
            ],
            model="claude-3-haiku-20240307",
        )
        assert response.content is not None
        assert len(response.content) > 0
    except AuthenticationError:
        pytest.fail("Authentication Error: The provided ANTHROPIC_API_KEY is invalid.")
    except Exception as e:
        pytest.fail(f"API call failed with an unexpected error: {str(e)}")

@pytest.mark.asyncio
async def test_generate_roadmap_dummy_structure():
    """
    Test that the dummy placeholder function returns the expected JSON structure.
    """
    result = await generate_roadmap_with_claude(missing_skills=["Python"], jd_text="Need Python dev")
    
    assert "roadmap" in result
    assert "message" in result
    assert isinstance(result["roadmap"], list)
    assert len(result["roadmap"]) > 0
    
    # Check the keys inside the first roadmap item
    first_item = result["roadmap"][0]
    assert "timeline" in first_item
    assert "focus" in first_item
    assert "resources" in first_item
