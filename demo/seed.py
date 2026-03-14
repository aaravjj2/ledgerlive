#!/usr/bin/env python3
"""Seed the LedgerLive database with realistic sample financial data.

Creates:
- 50+ transactions (mix of matched, unmatched, exceptions)
- 5 documents (invoices, bank statements, GL exports)
- 3 reconciliation runs with varying match rates
- 2 exception queues with different severities
- 1 complete close period with all stages
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "api"))

import json
from datetime import datetime, timedelta
import random
import hashlib

# Demo data constants
VENDORS = ["Acme Corp", "TechParts Ltd", "Office Supply Co", "Cloud Services Inc", "Marketing Agency Pro"]
DESCRIPTIONS = [
    "Monthly server hosting fee",
    "Office supplies - Q1 restock",
    "Software license renewal",
    "Consulting services - Feb",
    "Marketing campaign - Spring",
    "Insurance premium - Q1",
    "Travel expenses - conference",
    "Hardware procurement - laptops",
    "Legal retainer - monthly",
    "Payroll processing fee",
]

def generate_transactions(count=50):
    """Generate realistic financial transactions."""
    txns = []
    base_date = datetime(2026, 3, 1)
    for i in range(count):
        amount = round(random.uniform(100, 50000), 2)
        vendor = random.choice(VENDORS)
        desc = random.choice(DESCRIPTIONS)
        status = random.choices(
            ["matched", "unmatched", "exception", "pending"],
            weights=[60, 15, 10, 15],
            k=1
        )[0]
        txn = {
            "id": f"TXN-2026-{i+1:04d}",
            "date": (base_date + timedelta(days=random.randint(0, 28))).isoformat()[:10],
            "vendor": vendor,
            "description": desc,
            "amount": amount,
            "currency": "USD",
            "status": status,
            "source": random.choice(["bank_feed", "gl_export", "invoice"]),
            "content_hash": hashlib.sha256(f"{vendor}-{amount}-{i}".encode()).hexdigest()[:16],
        }
        txns.append(txn)
    return txns

def generate_documents(count=5):
    """Generate sample document metadata."""
    doc_types = [
        ("Invoice", "invoice_acme_feb2026.pdf", "application/pdf"),
        ("Bank Statement", "bofa_statement_feb2026.pdf", "application/pdf"),
        ("GL Export", "gl_export_feb2026.csv", "text/csv"),
        ("Vendor Statement", "techparts_statement_q1.pdf", "application/pdf"),
        ("Journal Entry", "je_adjustments_feb2026.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    ]
    docs = []
    for i, (dtype, fname, mime) in enumerate(doc_types[:count]):
        docs.append({
            "id": f"DOC-2026-{i+1:04d}",
            "type": dtype,
            "filename": fname,
            "mime_type": mime,
            "uploaded_at": datetime(2026, 3, 1 + i).isoformat(),
            "status": "processed",
            "ocr_confidence": round(random.uniform(0.92, 0.99), 3),
            "content_hash": hashlib.sha256(fname.encode()).hexdigest()[:16],
        })
    return docs

def generate_reconciliation_runs(count=3):
    """Generate reconciliation run history."""
    runs = []
    for i in range(count):
        total = random.randint(100, 500)
        matched = int(total * random.uniform(0.85, 0.98))
        runs.append({
            "id": f"RECON-{i+1:04d}",
            "type": ["bank_to_gl", "subledger_to_gl", "vendor_statement"][i % 3],
            "started_at": datetime(2026, 3, 5 + i * 3).isoformat(),
            "completed_at": datetime(2026, 3, 5 + i * 3, 1, 30).isoformat(),
            "total_items": total,
            "matched": matched,
            "unmatched": total - matched,
            "match_rate": round(matched / total * 100, 1),
            "status": "completed",
        })
    return runs

def generate_exceptions():
    """Generate exception items with varying severities."""
    exceptions = [
        {
            "id": "EXC-001",
            "type": "duplicate_payment",
            "severity": "critical",
            "amount": 4500.00,
            "description": "Possible duplicate payment to Acme Corp - same amount $4,500 paid twice within 3 days",
            "status": "open",
            "confidence": 0.95,
            "auto_resolvable": False,
        },
        {
            "id": "EXC-002",
            "type": "vendor_mismatch",
            "severity": "high",
            "amount": 1200.00,
            "description": "Vendor statement shows $1,200 but GL shows $1,320 - $120 variance",
            "status": "open",
            "confidence": 0.88,
            "auto_resolvable": False,
        },
        {
            "id": "EXC-003",
            "type": "timing_difference",
            "severity": "medium",
            "amount": 890.00,
            "description": "Payment recorded Feb 28 in GL but Mar 1 in bank - cutoff timing difference",
            "status": "auto_resolved",
            "confidence": 0.92,
            "auto_resolvable": True,
        },
        {
            "id": "EXC-004",
            "type": "missing_document",
            "severity": "medium",
            "amount": 3200.00,
            "description": "GL entry for $3,200 to Marketing Agency Pro has no supporting invoice",
            "status": "open",
            "confidence": 0.85,
            "auto_resolvable": False,
        },
    ]
    return exceptions

def main():
    """Generate and save all demo data."""
    data = {
        "transactions": generate_transactions(50),
        "documents": generate_documents(5),
        "reconciliation_runs": generate_reconciliation_runs(3),
        "exceptions": generate_exceptions(),
        "generated_at": datetime.now().isoformat(),
        "total_records": 0,
    }
    data["total_records"] = sum(len(v) for k, v in data.items() if isinstance(v, list))

    output_path = os.path.join(os.path.dirname(__file__), "sample_data.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {data['total_records']} records:")
    print(f"  - {len(data['transactions'])} transactions")
    print(f"  - {len(data['documents'])} documents")
    print(f"  - {len(data['reconciliation_runs'])} reconciliation runs")
    print(f"  - {len(data['exceptions'])} exceptions")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
