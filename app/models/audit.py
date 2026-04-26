# ============================================================
# CyberShield — Audit Log Model
# ============================================================

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class AuditAction(str, Enum):
    # Auth
    LOGIN_SUCCESS   = "auth.login.success"
    LOGIN_FAILED    = "auth.login.failed"
    LOGOUT          = "auth.logout"
    REGISTER        = "auth.register"
    PASSWORD_CHANGE = "auth.password.change"

    # Alerts
    ALERT_CREATED   = "alert.created"
    ALERT_RESOLVED  = "alert.resolved"
    ALERT_DELETED   = "alert.deleted"

    # Logs
    LOG_UPLOADED    = "log.uploaded"
    LOG_DELETED     = "log.deleted"

    # Admin
    USER_BANNED     = "admin.user.banned"
    RULE_CREATED    = "admin.rule.created"
    RULE_DELETED    = "admin.rule.deleted"

    # System
    EXPORT_CSV      = "system.export.csv"
    SETTINGS_CHANGED = "system.settings.changed"


class AuditSeverity(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class AuditLog(SQLModel, table=True):
    """
    Records every critical action performed in the system.
    Used for compliance, forensics and anomaly detection.
    """

    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Quem fez
    user_id:    Optional[int] = Field(default=None, index=True)
    username:   Optional[str] = Field(default=None, max_length=100)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=300)

    # O que fez
    action:   AuditAction  = Field(index=True)
    severity: AuditSeverity = Field(default=AuditSeverity.LOW)
    resource: Optional[str] = Field(default=None, max_length=200)
    detail:   Optional[str] = Field(default=None, max_length=1000)

    # Resultado
    success:  bool = Field(default=True)
    error_msg: Optional[str] = Field(default=None, max_length=500)

    # Quando
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class AuditLogCreate(SQLModel):
    user_id:    Optional[int] = None
    username:   Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    action:     AuditAction   = AuditAction.LOGIN_SUCCESS
    severity:   AuditSeverity = AuditSeverity.LOW
    resource:   Optional[str] = None
    detail:     Optional[str] = None
    success:    bool           = True
    error_msg:  Optional[str]  = None


class AuditLogRead(SQLModel):
    id:         int
    user_id:    Optional[int]
    username:   Optional[str]
    ip_address: Optional[str]
    action:     AuditAction
    severity:   AuditSeverity
    resource:   Optional[str]
    detail:     Optional[str]
    success:    bool
    created_at: datetime
