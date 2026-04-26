# ============================================================
# CyberShield — Password Strength Validator
# ============================================================

import re
from dataclasses import dataclass


@dataclass
class PasswordResult:
    valid: bool
    score: int          # 0-100
    strength: str       # weak / fair / strong / very strong
    feedback: list[str]


class PasswordValidator:
    """
    Validates password strength with scoring system.
    Score 0-40:  Weak
    Score 41-60: Fair
    Score 61-80: Strong
    Score 81+:   Very Strong
    """

    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> PasswordResult:
        feedback = []
        score = 0

        # Comprimento
        length = len(password)
        if length < cls.MIN_LENGTH:
            feedback.append(f"Use at least {cls.MIN_LENGTH} characters.")
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 15

        # Letra maiúscula
        if re.search(r"[A-Z]", password):
            score += 15
        else:
            feedback.append("Add at least one uppercase letter.")

        # Letra minúscula
        if re.search(r"[a-z]", password):
            score += 10
        else:
            feedback.append("Add at least one lowercase letter.")

        # Números
        digits = len(re.findall(r"\d", password))
        if digits >= 2:
            score += 20
        elif digits == 1:
            score += 10
            feedback.append("Add more numbers for a stronger password.")
        else:
            feedback.append("Add at least one number.")

        # Caracteres especiais
        specials = len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", password))
        if specials >= 2:
            score += 20
        elif specials == 1:
            score += 10
            feedback.append("Add more special characters.")
        else:
            feedback.append("Add special characters (!@#$%^&*).")

        # Penalidade por sequências óbvias
        if re.search(r"(012|123|234|345|456|567|678|789|890)", password):
            score -= 10
            feedback.append("Avoid sequential numbers.")
        if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi)", password, re.I):
            score -= 10
            feedback.append("Avoid sequential letters.")
        if re.search(r"(.)\1{2,}", password):
            score -= 10
            feedback.append("Avoid repeating characters.")

        score = max(0, min(100, score))
        valid = score >= 41 and length >= cls.MIN_LENGTH

        if score <= 40:
            strength = "weak"
        elif score <= 60:
            strength = "fair"
        elif score <= 80:
            strength = "strong"
        else:
            strength = "very strong"

        return PasswordResult(
            valid=valid,
            score=score,
            strength=strength,
            feedback=feedback,
        )
