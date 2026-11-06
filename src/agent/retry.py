"""One retry for LLM calls, mapping failures to FallbackRecord reasons (PROJECT_CONTEXT §5.4)."""
import inspect

from src.agent.llm_provider import LLMError, LLMTimeout


def _accepts_attempt(provider):
    params = inspect.signature(provider.complete).parameters.values()
    return any(p.name == "attempt" or p.kind is p.VAR_KEYWORD for p in params)


def complete_and_parse(provider, prompt, parse, max_retries=1, json_mode=True):
    """Call the provider and parse its answer, retrying up to max_retries times.

    Returns (parsed result, fallback reason, detail, attempts). On the first
    success the reason and detail are None. After the last failed attempt the
    last reason is returned: LLMTimeout -> "timeout", other LLMError ->
    "provider_error", InvalidJSONError -> "invalid_json",
    SchemaViolationError -> "schema_violation". Attempt a is passed to the
    provider (a retry uses another seed) when it supports it.
    """
    from src.agent.semantic_analyzer import InvalidJSONError, SchemaViolationError
    with_attempt = _accepts_attempt(provider)
    reason = detail = None
    attempts = 0
    for a in range(max_retries + 1):
        attempts += 1
        try:
            text = provider.complete(prompt, json_mode, attempt=a) if with_attempt else \
                provider.complete(prompt, json_mode)
            return parse(text), None, None, attempts
        except LLMTimeout as e:
            reason, detail = "timeout", str(e)
        except LLMError as e:
            reason, detail = "provider_error", str(e)
        except InvalidJSONError as e:
            reason, detail = "invalid_json", str(e)
        except SchemaViolationError as e:
            reason, detail = "schema_violation", str(e)
    return None, reason, detail, attempts
