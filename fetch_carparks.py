import json
import urllib.request

def get(url):
    with urllib.request.urlopen(url) as r:
        return json.load(r)

# Fetch car park info + vacancy
info = get("https://api.data.gov.hk/v1/carpark-info-vacancy?data=info&max=600")
vacancy = get("https://api.data.gov.hk/v1/carpark-info-vacancy?data=vacancy&max=600")

print(f"info results: {len(info.get('results', []))}")
print(f"vacancy results: {len(vacancy.get('results', []))}")
print()

# Build a map of park_Id -> car park
parks = {}
for p in info.get("results", []):
    parks[p["park_Id"]] = p

# Add EV vacancy and lastupdate from the vacancy feed
ev_free_count = 0
for v in vacancy.get("results", []):
    pid = v["park_Id"]
    if pid in parks:
        pc = v.get("privateCar") or []
        ev = next((c for c in pc if c.get("vacancy_type") == "A"), None)
        parks[pid]["_freeTotal"] = ev.get("vacancy") if ev else None
        parks[pid]["_lastupdate"] = pc[0].get("lastupdate") if pc else None
        if ev and int(ev.get("vacancy") or 0) > 0:
            ev_free_count += 1

print(f"Total car parks tracked: {len(parks)}")
print()

# List all car parks
print(f"{'No.':<4} {'park_Id':<20} {'Name':<40} {'District':<22} {'Free spaces':>11} {'Last update':<17}")
print("-" * 120)
for i, (pid, p) in enumerate(sorted(parks.items()), 1):
    name = p.get("name", "")
    district = p.get("district", "") or ""
    free_ev = p.get("_freeTotal")
    lastup = (p.get("_lastupdate") or "")[:16]
    print(f"{i:<4} {pid:<20} {name:<40} {district:<22} {str(free_ev):>8} {lastup:<17}")

print()
print(f"Total: {len(parks)} car parks tracked.")
