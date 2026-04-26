# ============================================================
# CyberShield — Integration Tests: Auth Endpoints
# ============================================================

from app.utils.password import PasswordValidator


class TestPasswordValidator:
    def test_weak_password(self):
        result = PasswordValidator.validate("123")
        assert result.valid is False
        assert result.strength == "weak"

    def test_strong_password(self):
        result = PasswordValidator.validate("Str0ng!Pass#99")
        assert result.valid is True
        assert result.strength in ["strong", "very strong"]

    def test_feedback_on_missing_uppercase(self):
        result = PasswordValidator.validate("lowercase123!")
        feedbacks = " ".join(result.feedback)
        assert "uppercase" in feedbacks.lower()

    def test_score_range(self):
        result = PasswordValidator.validate("AnyPassword123!")
        assert 0 <= result.score <= 100

    def test_sequential_penalty(self):
        weak = PasswordValidator.validate("Password123")
        strong = PasswordValidator.validate("P@ssw0rd!X9q")
        assert strong.score >= weak.score
