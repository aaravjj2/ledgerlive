"""GitLab Compliance Rule Engine for financial configuration changes.

Analyzes diffs to configuration files and returns compliance findings.
10 rules covering reconciliation tolerances, account mappings, exception flags,
and segregation of duties.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ComplianceFinding:
    rule_id: str
    rule_name: str
    severity: Severity
    description: str
    file_path: str
    line_number: Optional[int] = None
    recommendation: str = ""


@dataclass
class ComplianceReport:
    findings: list[ComplianceFinding] = field(default_factory=list)
    total_findings: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    requires_cfo_approval: bool = False
    energy_tier: str = "standard"  # standard | minimal (Green Agent)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["findings"] = [asdict(f) for f in self.findings]
        return d


# ── 10 Compliance Rules ──────────────────────────────────────

def _check_tolerance_increase(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 1: Increasing a reconciliation tolerance by >10% is HIGH risk."""
    findings = []
    pattern = r'[-]\s*tolerance\s*[:=]\s*([\d.]+).*\n[+]\s*tolerance\s*[:=]\s*([\d.]+)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        old_val = float(match.group(1))
        new_val = float(match.group(2))
        if old_val > 0 and ((new_val - old_val) / old_val) > 0.10:
            findings.append(ComplianceFinding(
                rule_id="COMP-001",
                rule_name="Tolerance Increase > 10%",
                severity=Severity.HIGH,
                description=f"Reconciliation tolerance increased from {old_val} to {new_val} ({((new_val-old_val)/old_val)*100:.1f}% increase)",
                file_path=file_path,
                recommendation="Justify the tolerance change with a documented business reason. Requires CFO review.",
            ))
    return findings


def _check_exception_flag_disabled(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 2: Disabling any exception flag is CRITICAL."""
    findings = []
    pattern = r'[-]\s*(exception_flag|flag_exceptions|auto_flag)\s*[:=]\s*(true|enabled|on|1).*\n[+]\s*\1\s*[:=]\s*(false|disabled|off|0)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        findings.append(ComplianceFinding(
            rule_id="COMP-002",
            rule_name="Exception Flag Disabled",
            severity=Severity.CRITICAL,
            description=f"Exception flag '{match.group(1)}' was disabled. This could mask financial discrepancies.",
            file_path=file_path,
            recommendation="Exception flags must not be disabled without CFO + audit committee approval.",
        ))
    return findings


def _check_account_code_change(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 3: Changing an account code mapping requires CFO approval."""
    findings = []
    if "accounts" in file_path.lower() or "chart_of_accounts" in file_path.lower() or "coa" in file_path.lower():
        pattern = r'[-]\s*(\w+_code|account_id|gl_code)\s*[:=]\s*(\S+).*\n[+]\s*\1\s*[:=]\s*(\S+)'
        for match in re.finditer(pattern, diff, re.IGNORECASE):
            findings.append(ComplianceFinding(
                rule_id="COMP-003",
                rule_name="Account Code Mapping Change",
                severity=Severity.HIGH,
                description=f"Account code '{match.group(1)}' changed from {match.group(2)} to {match.group(3)}",
                file_path=file_path,
                recommendation="Account code changes require CFO sign-off and audit trail entry.",
            ))
    return findings


def _check_materiality_threshold(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 4: Raising materiality threshold above $10K is CRITICAL."""
    findings = []
    pattern = r'[+]\s*materiality[_\s]*threshold\s*[:=]\s*([\d.]+)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        val = float(match.group(1))
        if val > 10000:
            findings.append(ComplianceFinding(
                rule_id="COMP-004",
                rule_name="Materiality Threshold Elevated",
                severity=Severity.CRITICAL,
                description=f"Materiality threshold set to ${val:,.2f}, above the $10,000 audit limit",
                file_path=file_path,
                recommendation="Materiality changes above $10K require audit committee approval.",
            ))
    return findings


def _check_auto_approve_enabled(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 5: Enabling auto-approve for any workflow is HIGH risk."""
    findings = []
    pattern = r'[+]\s*(auto_approve|skip_review|bypass_approval)\s*[:=]\s*(true|enabled|on|1)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        findings.append(ComplianceFinding(
            rule_id="COMP-005",
            rule_name="Auto-Approve Enabled",
            severity=Severity.HIGH,
            description=f"Auto-approve setting '{match.group(1)}' was enabled",
            file_path=file_path,
            recommendation="Auto-approval bypasses segregation of duties. Requires documented exception.",
        ))
    return findings


def _check_retention_period_reduced(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 6: Reducing data retention period is MEDIUM risk."""
    findings = []
    pattern = r'[-]\s*retention[_\s]*(?:period|days)\s*[:=]\s*(\d+).*\n[+]\s*retention[_\s]*(?:period|days)\s*[:=]\s*(\d+)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        old_val = int(match.group(1))
        new_val = int(match.group(2))
        if new_val < old_val:
            findings.append(ComplianceFinding(
                rule_id="COMP-006",
                rule_name="Retention Period Reduced",
                severity=Severity.MEDIUM,
                description=f"Data retention reduced from {old_val} to {new_val} days",
                file_path=file_path,
                recommendation="Verify the new retention period meets regulatory requirements (SOX: 7 years).",
            ))
    return findings


def _check_encryption_disabled(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 7: Disabling encryption is CRITICAL."""
    findings = []
    pattern = r'[+]\s*(encrypt|encryption|tls|ssl)\s*[:=]\s*(false|disabled|off|none|0)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        findings.append(ComplianceFinding(
            rule_id="COMP-007",
            rule_name="Encryption Disabled",
            severity=Severity.CRITICAL,
            description=f"Encryption setting '{match.group(1)}' was disabled",
            file_path=file_path,
            recommendation="Encryption must remain enabled for all financial data in transit and at rest.",
        ))
    return findings


def _check_role_escalation(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 8: Adding admin/superuser role is HIGH risk."""
    findings = []
    pattern = r'[+]\s*(role|permission|access_level)\s*[:=]\s*(admin|superuser|root|owner)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        findings.append(ComplianceFinding(
            rule_id="COMP-008",
            rule_name="Role Escalation",
            severity=Severity.HIGH,
            description=f"Elevated role '{match.group(2)}' added to configuration",
            file_path=file_path,
            recommendation="Role escalations must follow least-privilege principle. Document the business need.",
        ))
    return findings


def _check_audit_trail_config(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 9: Modifying audit trail settings is MEDIUM risk."""
    findings = []
    if any(kw in diff.lower() for kw in ["audit_trail", "audit_log", "logging_level"]):
        pattern = r'[-]\s*(audit|log)\S*\s*[:=]\s*\S+.*\n[+]\s*\1\S*\s*[:=]\s*\S+'
        for match in re.finditer(pattern, diff, re.IGNORECASE):
            findings.append(ComplianceFinding(
                rule_id="COMP-009",
                rule_name="Audit Trail Configuration Changed",
                severity=Severity.MEDIUM,
                description="Audit trail configuration was modified",
                file_path=file_path,
                recommendation="Audit trail changes require security team review.",
            ))
    return findings


def _check_new_external_integration(diff: str, file_path: str) -> list[ComplianceFinding]:
    """Rule 10: Adding a new external API endpoint is LOW risk."""
    findings = []
    pattern = r'[+]\s*(api_url|endpoint|webhook_url|external_url)\s*[:=]\s*(\S+)'
    for match in re.finditer(pattern, diff, re.IGNORECASE):
        findings.append(ComplianceFinding(
            rule_id="COMP-010",
            rule_name="New External Integration",
            severity=Severity.LOW,
            description=f"New external integration endpoint added: {match.group(2)}",
            file_path=file_path,
            recommendation="Verify the external service has passed vendor security assessment.",
        ))
    return findings


ALL_RULES = [
    _check_tolerance_increase,
    _check_exception_flag_disabled,
    _check_account_code_change,
    _check_materiality_threshold,
    _check_auto_approve_enabled,
    _check_retention_period_reduced,
    _check_encryption_disabled,
    _check_role_escalation,
    _check_audit_trail_config,
    _check_new_external_integration,
]


def check_compliance(diff: str, file_path: str = "unknown") -> ComplianceReport:
    """Run all compliance rules against a config diff.

    Args:
        diff: Unified diff string of the configuration change
        file_path: Path to the changed file

    Returns:
        ComplianceReport with all findings
    """
    report = ComplianceReport()

    for rule_fn in ALL_RULES:
        findings = rule_fn(diff, file_path)
        report.findings.extend(findings)

    report.total_findings = len(report.findings)
    report.critical_count = sum(1 for f in report.findings if f.severity == Severity.CRITICAL)
    report.high_count = sum(1 for f in report.findings if f.severity == Severity.HIGH)
    report.medium_count = sum(1 for f in report.findings if f.severity == Severity.MEDIUM)
    report.low_count = sum(1 for f in report.findings if f.severity == Severity.LOW)
    report.requires_cfo_approval = report.critical_count > 0 or report.high_count > 0

    # Green Agent: tiered inference
    if report.critical_count > 0 or report.high_count > 0:
        report.energy_tier = "full"  # Use Claude/Gemini for deep analysis
    else:
        report.energy_tier = "minimal"  # Use smaller model or skip LLM

    return report
