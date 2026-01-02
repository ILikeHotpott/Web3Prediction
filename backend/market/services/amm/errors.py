class QuoteError(ValueError):
    """Base quote error."""


class QuoteNotFoundError(QuoteError):
    """Market/pool/state not found."""


class QuoteInputError(QuoteError):
    """Bad inputs."""


class QuoteMathError(QuoteError):
    """Math/feasibility issues."""

