# ============================================================
# CyberShield — Input Sanitization Utils
# ============================================================

import re
import html


class Sanitizer:
    """
    Sanitizes and validates user inputs before processing.
    Prevents XSS, path traversal and common injection patterns.
    """

    # Padrões suspeitos comuns
    DANGEROUS_PATTERNS = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"(\.\./){2,}",          # path traversal
        r"(UNION|SELECT|INSERT|UPDATE|DELETE|DROP)\s",  # SQLi básico
        r"(exec|eval|system|shell_exec)\s*\(",          # RCE
    ]

    _compiled = [
        re.compile(p, re.IGNORECASE | re.DOTALL)
        for p in DANGEROUS_PATTERNS
    ]

    @classmethod
    def clean_string(cls, value: str, max_length: int = 500) -> str:
        """Remove HTML, trunca e escapa caracteres perigosos."""
        if not isinstance(value, str):
            return ""
        value = value.strip()
        value = value[:max_length]
        value = html.escape(value)
        return value

    @classmethod
    def is_suspicious(cls, value: str) -> bool:
        """Retorna True se o valor contém padrões perigosos."""
        for pattern in cls._compiled:
            if pattern.search(value):
                return True
        return False

    @classmethod
    def sanitize_log_entry(cls, entry: dict) -> dict:
        """Sanitiza todos os campos string de um log entry."""
        sanitized = {}
        for key, val in entry.items():
            if isinstance(val, str):
                sanitized[key] = cls.clean_string(val)
            else:
                sanitized[key] = val
        return sanitized

    @classmethod
    def extract_ip(cls, raw: str) -> str | None:
        """Extrai e valida um endereço IP de uma string."""
        pattern = re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
        )
        match = pattern.search(raw)
        return match.group() if match else None
