# HK Car Park Vacancy — Live Dashboard

A self-contained, browser-based dashboard showing near-real-time public car park
vacancy data for Hong Kong from data.gov.hk (Transport Department + EKEO).

Live URL (default): <http://localhost:8124/index.html>

## Features

- Live map with one coloured marker per car park (Leaflet + OpenStreetMap) and clickable popups
- Top-12 bar chart of free spaces (Chart.js)
- 5 KPI cards: parks tracked, total free, EV-feed parks, free EV spaces, districts covered
- Filter tabs: All car parks / EV only / Non-EV
- District dropdown (18 districts), sorting (district / most free / name), instant search with result counter
- Three languages: English, 繁體中文, 简体中文 (UI strings + API-returned park names/districts)
- Auto-refresh every 60 seconds; filter, district, sort and search selections persist across refresh
- Correct handling of the API's `vacancy = -1` sentinel ("no operator data") — shown as `n/a`, never a negative count
- Responsive layout: desktop, laptop, tablet and mobile; search box expands to full width on small screens

## Files

| File | Purpose |
|------|---------|
| `index.html` | The entire dashboard (HTML + CSS + JavaScript in one file). No build step. |
| `fetch_carparks.py` | Optional helper: prints a plain-text list of all car parks with free spaces and update times. |
| `carparks_list.txt` | A previously generated snapshot of that list (591 rows). Not used by the dashboard. |

## Software dependencies

Runtime (to view the dashboard):

- **Python 3** (any recent version; only the standard library is used for the server)
- **A modern web browser** with JavaScript enabled (Chrome, Edge, Firefox, Safari)
- **Internet access** from the browser to:
  - `api.data.gov.hk` — live car park data (CORS-enabled, no API key needed)
  - `unpkg.com` — Leaflet library and CSS
  - `cdn.jsdelivr.net` — Chart.js library
  - `tile.openstreetmap.org` — map tiles

Optional (to regenerate `carparks_list.txt`):

- **Python 3.6+** — `fetch_carparks.py` uses only the standard library (`json`, `urllib.request`); no `pip install` needed.

No npm, Node.js, database, API key or backend service is required.

## How to run

1. Open a terminal in the folder containing these files.

2. Start a local web server:

   ```bash
   python3 -m http.server 8124
   ```

3. Open a browser and go to:

   - On the same machine: <http://localhost:8124/index.html>
   - From another device on the same network: <http://YOUR-IP-ADDRESS:8124/index.html>
     (find your machine's IP with `hostname -I` on Linux or `ipconfig` on Windows)

4. Data loads automatically within a few seconds; it refreshes every 60 seconds.

To run detached (keeps running after the terminal is closed):

```bash
nohup python3 -m http.server 8124 > /tmp/hk-carpark-serve.log 2>&1 &
```

Stop the server with `Ctrl+C` in the foreground terminal, or `pkill -f "http.server 8124"`.

## Optional: regenerate the car park list

```bash
python3 fetch_carparks.py > carparks_list.txt
```

This fetches the current info + vacancy feeds and writes a plain-text table.
The dashboard itself does **not** read this file — it fetches live data directly.

## Data source and semantics

- Endpoint: `https://api.data.gov.hk/v1/carpark-info-vacancy`
  - `?data=info&max=600` — names, districts, coordinates, facilities
  - `?data=vacancy&max=600` — availability, EV spaces, last update
  - `&lang=en_US|zh_TW|zh_CN` — language of names/districts
- `privateCar[].vacancy`: available spaces. Per the official spec:
  - type `A`: actual number; `-1` = operator did not provide data; `0` = full
  - type `B`: `1` = spaces available (no count), `0` = full, `-1` = no data
  - type `C`: closed
- `vacancyEV`: EV-only spaces; present for only ~11 parks
- `lastupdate`: per-car-park timestamp (HKT)
- District names are normalised by stripping the ` District` / `區` suffix; `Islands` is displayed as `Islands(Tung Chung)` / `離島區(東涌)` / `离岛区(东涌)`
- Attribution: HKSAR Government, Transport Department and Energizing Kowloon East Office

## Configuration (edit `index.html`)

- `var API = ...` — data endpoint
- `var REFRESH_MS = 60000` — auto-refresh interval (milliseconds)
- `I18N` object — all translated UI strings
- `districtLabel(d)` — custom district display names
- `parseFree()` / `parseEv()` — how raw API values are interpreted

## Troubleshooting

- **Stale page / changes not visible:** hard-refresh with `Ctrl+F5`, or append a version query like `?v=5` to the URL. The page sends no-cache headers, but browsers can still cache.
- **Search appears not to filter:** make sure you are opening `index.html` through the local web server (port **8124**), not by double-clicking the file. Type in the box next to the 🔍 icon — the result counter beside it updates instantly.
- **Map shows "Map library unavailable":** the CDN for Leaflet is blocked. The list and chart still work. Allow `unpkg.com`.
- **Chart missing:** allow `cdn.jsdelivr.net`.
- **Cannot open from another device:** confirm both devices are on the same network, the server is bound to `0.0.0.0` (the default of `python3 -m http.server`), and no firewall blocks port 8124.
- **Port already in use:** stop the existing server or change both the server port and the URL.

## Disclaimer / 免責聲明

**English:** This dashboard is provided for informational purposes only. The car park data is sourced from data.gov.hk (Transport Department and Energizing Kowloon East Office, HKSAR Government). I am not the owner of the data and make no representation or warranty as to its accuracy, completeness, integrity, timeliness or fitness for any purpose. I accept no responsibility or liability for any errors, omissions, delays, or for any decision made in reliance on the information shown here. Please verify against the official source before relying on it.

**繁體中文:** 本儀表板僅供參考。停車場數據取自 data.gov.hk（香港特別行政區政府運輸署及東九龍總區辦事處）。筆者並非數據擁有者，對數據的準確性、完整性、真確性、及時性或適用性不作任何保證，亦不對任何錯誤、遺漏、延誤或依賴本資訊而作出的決定承擔任何責任。使用請以官方資料為準。

**简体中文:** 本仪表板仅供参考。停车场数据取自 data.gov.hk（香港特别行政区政府运输署及东九龙总区办事处）。作者并非数据拥有者，对数据的准确性、完整性、真实性、及时性或适用性不作任何保证，也不对任何错误、遗漏、延误或依赖本信息而作出的决定承担任何责任。请以官方资料为准。

## Licence / attribution

Data © HKSAR Government. Dashboard code is a local, personal project; no credentials or API keys are stored in any file.
