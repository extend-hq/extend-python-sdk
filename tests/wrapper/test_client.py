"""Tests for the Extend/AsyncExtend wrapper clients' token handling."""

import pytest

from extend_ai import AsyncExtend, Extend
from extend_ai.core.api_error import ApiError


@pytest.mark.parametrize("client_cls", [Extend, AsyncExtend])
class TestTokenEnvFallback:
    """The wrapper must honor EXTEND_API_KEY like the generated client does."""

    def test_falls_back_to_env_var(self, client_cls, monkeypatch):
        """Bare construction should pick up EXTEND_API_KEY."""
        monkeypatch.setenv("EXTEND_API_KEY", "env-test-key")

        client = client_cls()

        assert client._client_wrapper._get_token() == "env-test-key"

    def test_explicit_token_wins_over_env_var(self, client_cls, monkeypatch):
        """An explicit token= argument should take precedence."""
        monkeypatch.setenv("EXTEND_API_KEY", "env-test-key")

        client = client_cls(token="explicit-key")

        assert client._client_wrapper._get_token() == "explicit-key"

    def test_raises_api_error_when_no_token_anywhere(self, client_cls, monkeypatch):
        """No token and no env var should raise the generated client's ApiError."""
        monkeypatch.delenv("EXTEND_API_KEY", raising=False)

        with pytest.raises(ApiError, match="EXTEND_API_KEY"):
            client_cls()
