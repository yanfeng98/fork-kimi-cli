from __future__ import annotations


class KimiCLIException(Exception):
    pass


class ConfigError(KimiCLIException, ValueError):
    """Configuration error."""

    pass


class AgentSpecError(KimiCLIException, ValueError):
    pass


class InvalidToolError(KimiCLIException, ValueError):
    """Invalid tool error."""

    pass


class MCPConfigError(KimiCLIException, ValueError):
    """MCP config error."""

    pass


class MCPRuntimeError(KimiCLIException, RuntimeError):
    """MCP runtime error."""

    pass
