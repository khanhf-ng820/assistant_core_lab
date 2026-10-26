"""The shared error hierarchy must be catchable at the service boundary."""

import pytest

from assistant_core.errors import AssistantError, ConfigError, DataError, InvalidRequest, ProviderError


@pytest.mark.parametrize("error_type", [ConfigError, DataError, InvalidRequest, ProviderError])
def test_named_error_is_an_assistant_error(error_type):
    with pytest.raises(AssistantError, match="operation failed"):
        raise error_type("operation failed")
