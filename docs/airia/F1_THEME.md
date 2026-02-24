# F1 Theme — Finance Close Metaphor

## Why F1?

Formula 1 is the highest-stakes, most telemetry-rich, most time-critical operation in sport.
Month-end financial close is the same for a finance organisation:

- **Hard deadline** — markets wait for no one; auditors neither
- **Multi-team coordination** — AP, AR, treasury, intercompany, tax, FP&A all run in parallel
- **Fail-closed safety** — you cannot reopen the year because a payment crossing was wrong
- **Evidence-first** — every decision must be auditable; the stewards (external auditors) will check

LedgerLive maps the F1 pit-wall metaphor across the entire close workflow so that executives,
engineers, and auditors share a single vocabulary.

## Full Term Mapping

| F1 Term | Finance Reality | LedgerLive Feature |
|---------|-----------------|-------------------|
| Race Control | Close Command Center | `/race-control` dashboard |
| Lap | Close Stage / Milestone | Wave batch completion |
| Pit Stop | Scheduled Close Checkpoint | HITL approval gate |
| Pit Wall | Approver chain + SLA escalation | Review Queue page |
| Telemetry | Tool trace + audit log + drift budget | Audit Log page |
| Incident | Exception / blocker / policy event | Exceptions page |
| Safety Car | Fail-closed + approvals required | Guard middleware |
| DRS Zone | Fast-path auto-approval | Straight-through processing rule |
| Court Pack | Stewards evidence package | Evidence Binder PDF |
| Stewards | External auditors | Audit trail readers |
| Qualifying | Pre-close trial run | Golden Scenario seed |
| Marshal Flag | SLA alert / escalation trigger | Exception severity badge |
| Scrutineering | Financial control checklist | Gate assertions |
| Podium | Period closed, signed, filed | Close completion badge |

## F1 Badge in the UI

The Race Control page header shows:

```
🏁  Race Beyond the Track
```

with `data-testid="f1-theme-badge"` — a permanent brand mark visible to judges and users.

## Narrative

> The finance close process starts 30 days before the end of the period. Sub-ledger feeds arrive
> like data from the car's sensors — streams of AP invoices, AR settlements, payroll accruals,
> intercompany entries. Race Control sees them all.
>
> When a variance surfaces, it's an incident. The Safety Car deploys — no further approvals
> proceed until the triage team clears it. When cleared, the DRS zone opens for straight-through
> processing of within-threshold items.
>
> At each pit stop (checkpoint), the pit wall (approver chain) must confirm readiness. Miss a
> stop and the car DNFs — the period cannot close.
>
> At the chequered flag, the evidence binder is sealed, sha256 assertions are logged, and the
> court pack is ready for the stewards (external auditors).

## Williams F1 Connection

LedgerLive was built for the **Airia × Williams F1 Hackathon**. Williams Racing's transformation
to a data-driven operation — from pit-wall telemetry to strategy simulation — mirrors the
transformation LedgerLive delivers for finance operations teams.
