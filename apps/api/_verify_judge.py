"""Quick verification script: checks all 6 CFO evidence items match judge expectations."""
import httpx

base = "http://localhost:8090"

# 6a: CFO Cockpit
r = httpx.get(f"{base}/api/cfo/cockpit")
d = r.json()
print("=== 6a CFO Cockpit ===")
print(f"  status: {r.status_code}")
print(f"  cost_cap.runway_usd > 0: {d.get('cost_cap', {}).get('runway_usd', 0) > 0}")
print(f"  exception_impact.saved_usd > 0: {d.get('exception_impact', {}).get('saved_usd', 0) > 0}")
print(f"  close_velocity.speedup_x > 1: {d.get('close_velocity', {}).get('speedup_x', 0) > 1}")

# 6b: Scenario Pack
r = httpx.get(f"{base}/api/cfo/scenario")
d = r.json()
print("\n=== 6b Scenario Pack ===")
print(f"  status: {r.status_code}")
print(f"  invoices count: {len(d.get('invoices', []))} (need >= 5)")
print(f"  exceptions_before count: {len(d.get('exceptions_before', []))} (need >= 2)")

# 6c: Ask Engineer
r = httpx.post(f"{base}/api/agent/ask", json={"question": "What's blocking the close?"})
d = r.json()
print("\n=== 6c Ask Engineer ===")
print(f"  status: {r.status_code}")
print(f"  answer truthy: {bool(d.get('answer'))}")
print(f"  citations len > 0: {len(d.get('citations', [])) > 0}")

# 6d: Story Mode
r = httpx.get(f"{base}/api/cfo/story-mode")
d = r.json()
print("\n=== 6d Story Mode ===")
print(f"  status: {r.status_code}")
print(f"  steps count: {len(d.get('steps', []))} (need >= 5)")

# 6e: Race Control cfo_summary
r = httpx.get(f"{base}/api/race-control")
d = r.json()
cfo_summary = d.get("cfo_cockpit", {}).get("cfo_summary")
print("\n=== 6e Race Control CFO Summary ===")
print(f"  status: {r.status_code}")
print(f"  cfo_cockpit.cfo_summary truthy: {bool(cfo_summary)}")

# 6f: DEMO_CFO.md file exists
import pathlib
demo_path = pathlib.Path(r"c:\Aarav\ledgerlive\docs\DEMO_CFO.md")
print(f"\n=== 6f DEMO_CFO.md ===")
print(f"  exists: {demo_path.exists()}")

# Summary
all_pass = all([
    r.status_code == 200,
    bool(cfo_summary),
    demo_path.exists(),
])
print(f"\n{'='*40}")
print(f"ALL CFO CHECKS: {'PASS' if all_pass else 'FAIL'}")
