#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mileage Calculator – Local Python GUI
- FreeSimpleGUI UI (imports from local fallback if not installed)
- Always uses settings.json located next to this script
- Distance-band engine + Business-Class city/region overrides
- Adjustable ratio, transfer bonus, passengers, expiry date
"""
import os
import sys
import json
import math
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

# Use FreeSimpleGUI; fall back to your local folder if needed
try:
    import FreeSimpleGUI as sg
except ImportError:
    sys.path.insert(0, r"C:\mileage_UOB\FreeSimpleGUI-main")
    import FreeSimpleGUI as sg

APP_NAME = "Mileage Calculator (Local GUI)"

# Always put settings.json in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "settings.json")

# ------------------------------
# Airports (expanded)
# ------------------------------
AIRPORTS = {
    "BKK": {"iata": "BKK", "city": "Bangkok", "country": "Thailand", "lat": 13.690, "lon": 100.750},
    "HND": {"iata": "HND", "city": "Tokyo (Haneda)", "country": "Japan", "lat": 35.5494, "lon": 139.7798},
    "NRT": {"iata": "NRT", "city": "Tokyo (Narita)", "country": "Japan", "lat": 35.7647, "lon": 140.3864},
    "KIX": {"iata": "KIX", "city": "Osaka", "country": "Japan", "lat": 34.4273, "lon": 135.2440},
    "ICN": {"iata": "ICN", "city": "Seoul", "country": "South Korea", "lat": 37.4602, "lon": 126.4407},
    "HKG": {"iata": "HKG", "city": "Hong Kong", "country": "Hong Kong", "lat": 22.3080, "lon": 113.9185},
    "SIN": {"iata": "SIN", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915},
    "DOH": {"iata": "DOH", "city": "Doha", "country": "Qatar", "lat": 25.2731, "lon": 51.6081},
    "HEL": {"iata": "HEL", "city": "Helsinki", "country": "Finland", "lat": 60.3172, "lon": 24.9633},
    "LHR": {"iata": "LHR", "city": "London", "country": "United Kingdom", "lat": 51.4700, "lon": -0.4543},
    "CDG": {"iata": "CDG", "city": "Paris", "country": "France", "lat": 49.0097, "lon": 2.5479},
    "FRA": {"iata": "FRA", "city": "Frankfurt", "country": "Germany", "lat": 50.0379, "lon": 8.5622},
    "SYD": {"iata": "SYD", "city": "Sydney", "country": "Australia", "lat": -33.9399, "lon": 151.1753},
    "MEL": {"iata": "MEL", "city": "Melbourne", "country": "Australia", "lat": -37.6690, "lon": 144.8410},
    "TPE": {"iata": "TPE", "city": "Taipei", "country": "Taiwan", "lat": 25.0797, "lon": 121.2340},
    "DEL": {"iata": "DEL", "city": "Delhi", "country": "India", "lat": 28.5562, "lon": 77.1000},
    "JNB": {"iata": "JNB", "city": "Johannesburg", "country": "South Africa", "lat": -26.1392, "lon": 28.2460},
    "IST": {"iata": "IST", "city": "Istanbul", "country": "Türkiye", "lat": 41.2753, "lon": 28.7519},
    "LAX": {"iata": "LAX", "city": "Los Angeles", "country": "United States", "lat": 33.9416, "lon": -118.4085},
    "PVG": {"iata":"PVG","city":"Shanghai (Pudong)","country":"China","lat":31.1434,"lon":121.8052},
    "SHA": {"iata":"SHA","city":"Shanghai (Hongqiao)","country":"China","lat":31.1979,"lon":121.3363},
    "PEK": {"iata":"PEK","city":"Beijing (Capital)","country":"China","lat":40.0799,"lon":116.6031},
    "PKX": {"iata":"PKX","city":"Beijing (Daxing)","country":"China","lat":39.5099,"lon":116.4108},
    "FUK": {"iata":"FUK","city":"Fukuoka","country":"Japan","lat":33.5859,"lon":130.4500},
    "NGO": {"iata":"NGO","city":"Nagoya (Chubu)","country":"Japan","lat":34.8584,"lon":136.8054},
    "CTS": {"iata":"CTS","city":"Sapporo (Chitose)","country":"Japan","lat":42.7752,"lon":141.6923},
    "GMP": {"iata":"GMP","city":"Seoul (Gimpo)","country":"South Korea","lat":37.5583,"lon":126.7906},
}

# ------------------------------
# Destination groups
# ------------------------------
DEST_GROUPS = {
    "SHANGHAI": ["PVG", "SHA"],
    "BEIJING": ["PEK", "PKX"],
    "KIX FUK NGO": ["KIX", "FUK", "NGO"],
    "HND NRT CTS": ["HND", "NRT", "CTS"],
    "KOREA": ["ICN", "GMP"],
}

# ------------------------------
# Fixed Business Class overrides per program
# ------------------------------
ROUTE_BC_OVERRIDES = {
    "Asia Miles": {
        "SHANGHAI": 28000,
        "BEIJING": 28000,
        "KIX FUK NGO": 32000,
        "HND NRT CTS": 58000,
        "KOREA": 28000,
    },
    "Royal Orchid Plus": {
        "SHANGHAI": 30000,
        "BEIJING": 47500,
        "KIX FUK NGO": 47500,
        "HND NRT CTS": 47500,
        "KOREA": 47500,
    },
    "KrisFlyer": {
        "SHANGHAI": 43000,
        "BEIJING": 43000,
        "KIX FUK NGO": 52000,
        "HND NRT CTS": 52000,
        "KOREA": 52000,
    },
    "Avios": {
        "SHANGHAI": 33000,
        "BEIJING": 38500,
        "KIX FUK NGO": 46500,
        "HND NRT CTS": 46500,
        "KOREA": 38500,
    },
    "EVA": {
        "SHANGHAI": 25000,
        "BEIJING": 25000,
        "KIX FUK NGO": 25000,
        "HND NRT CTS": 25000,
        "KOREA": 25000,
    },
}

# ------------------------------
# Demo distance bands (Economy/Business) – replace with real charts as needed
# ------------------------------
DEMO_RATE_TABLES = {
    "Asia Miles": {
        "own": [
            {"max": 750, "Y": 7500, "J": 16000},
            {"max": 2750, "Y": 12000, "J": 30000},
            {"max": 5000, "Y": 20000, "J": 50000},
            {"max": 7500, "Y": 30000, "J": 70000},
            {"max": 1e12, "Y": 42000, "J": 90000},
        ],
        "partner": [
            {"max": 750, "Y": 9000, "J": 20000},
            {"max": 2750, "Y": 16000, "J": 36000},
            {"max": 5000, "Y": 26000, "J": 60000},
            {"max": 7500, "Y": 36000, "J": 80000},
            {"max": 1e12, "Y": 52000, "J": 100000},
        ],
        "homeAirline": "Cathay Pacific",
        "validity_months": 36,
        "ratio_multiplier": 1.00,
    },
    "KrisFlyer": {
        "own": [
            {"max": 750, "Y": 8500, "J": 17000},
            {"max": 2750, "Y": 14000, "J": 34000},
            {"max": 5000, "Y": 22000, "J": 52000},
            {"max": 7500, "Y": 32000, "J": 76000},
            {"max": 1e12, "Y": 50000, "J": 98000},
        ],
        "partner": [
            {"max": 750, "Y": 10000, "J": 22000},
            {"max": 2750, "Y": 18000, "J": 38000},
            {"max": 5000, "Y": 28000, "J": 64000},
            {"max": 7500, "Y": 38000, "J": 88000},
            {"max": 1e12, "Y": 56000, "J": 110000},
        ],
        "homeAirline": "Singapore Airlines",
        "validity_months": 36,
        "ratio_multiplier": 1.00,
    },
    "Qatar Privilege Club": {
        "own": [
            {"max": 750, "Y": 9000, "J": 18000},
            {"max": 2750, "Y": 14000, "J": 32000},
            {"max": 5000, "Y": 22000, "J": 52000},
            {"max": 7500, "Y": 32000, "J": 72000},
            {"max": 1e12, "Y": 46000, "J": 92000},
        ],
        "partner": [
            {"max": 750, "Y": 10000, "J": 20000},
            {"max": 2750, "Y": 16000, "J": 36000},
            {"max": 5000, "Y": 26000, "J": 60000},
            {"max": 7500, "Y": 34000, "J": 82000},
            {"max": 1e12, "Y": 50000, "J": 102000},
        ],
        "homeAirline": "Qatar Airways",
        "validity_months": 36,
        "ratio_multiplier": 1.00,
    },
    "Royal Orchid Plus": {
        "own": [
            {"max": 750, "Y": 10000, "J": 20000},
            {"max": 2750, "Y": 16000, "J": 38000},
            {"max": 5000, "Y": 26000, "J": 64000},
            {"max": 7500, "Y": 36000, "J": 90000},
            {"max": 1e12, "Y": 52000, "J": 120000},
        ],
        "partner": [
            {"max": 750, "Y": 11000, "J": 22000},
            {"max": 2750, "Y": 18000, "J": 42000},
            {"max": 5000, "Y": 30000, "J": 70000},
            {"max": 7500, "Y": 42000, "J": 100000},
            {"max": 1e12, "Y": 58000, "J": 130000},
        ],
        "homeAirline": "Thai Airways",
        "validity_months": 36,
        "ratio_multiplier": 1.00,
    },
}

DEFAULT_SETTINGS = {
    "programs": DEMO_RATE_TABLES,
    "airports": AIRPORTS,
    "origin": "BKK",
}

# ------------------------------
# Helpers
# ------------------------------
def load_settings() -> Dict[str, Any]:
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=2)
        return DEFAULT_SETTINGS
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def haversine_miles(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    R = 3958.7613
    from math import radians, sin, cos, atan2, sqrt
    dlat = radians(b["lat"] - a["lat"])
    dlon = radians(b["lon"] - a["lon"])
    lat1 = radians(a["lat"]); lat2 = radians(b["lat"])
    h = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(h), sqrt(1-h))
    return R * c

def band_price(bands: List[Dict[str, Any]], dist: float) -> Tuple[int, int]:
    for band in bands:
        if dist <= band["max"]:
            return band["Y"], band["J"]
    last = bands[-1]
    return last["Y"], last["J"]

def add_months(dt: datetime, months: int) -> datetime:
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return dt.replace(year=year, month=month, day=day)

def find_dest_group(iata: str) -> Optional[str]:
    for label, iatas in DEST_GROUPS.items():
        if iata in iatas:
            return label
    return None

def override_business_miles(program: str, dest_iata: str) -> Optional[int]:
    label = find_dest_group(dest_iata)
    if not label:
        return None
    prog_map = ROUTE_BC_OVERRIDES.get(program, {})
    return prog_map.get(label)

# ------------------------------
# UI
# ------------------------------
def build_layout(settings: Dict[str, Any]):
    programs = sorted(settings["programs"].keys())
    airports = settings["airports"]
    airport_keys = sorted(airports.keys())

    calc_col = [
        [sg.Text("Program", size=(12,1)), sg.Combo(programs, default_value=programs[0] if programs else "", key="-PROGRAM-", readonly=True, size=(28,1))],
        [sg.Text("Cabin", size=(12,1)), sg.Combo(["Economy", "Business"], default_value="Economy", key="-CABIN-", readonly=True, size=(28,1))],
        [sg.HorizontalSeparator()],
        [sg.Text("Passengers", size=(12,1)), sg.Spin([i for i in range(1,10)], initial_value=1, key="-PAX-", size=(6,1))],
        [sg.Text("Transfer bonus %", size=(12,1)), sg.Input(key="-BONUS-", size=(10,1), default_text="0"), sg.Text(" (e.g., 20 = +20%)")],
        [sg.Text("Future ratio ×", size=(12,1)), sg.Input(key="-RATIO-", size=(10,1), default_text="1.00"), sg.Text(" (multiplier)")],
        [sg.HorizontalSeparator()],
        [sg.Text("Origin IATA", size=(12,1)), sg.Combo(airport_keys, default_value=settings.get("origin","BKK"), key="-ORIGIN-", readonly=True, size=(10,1))],
        [sg.Text("Destination IATA", size=(12,1)), sg.Combo(airport_keys, default_value="HND", key="-DEST-", readonly=False, size=(10,1))],
        [sg.Checkbox("Use distance-based estimate", default=True, key="-USE_DIST-")],
        [sg.Text("OR miles per person", size=(12,1)), sg.Input(key="-MILES_MANUAL-", size=(12,1), default_text="")],
        [sg.HorizontalSeparator()],
        [sg.Text("Operating airline", size=(12,1)), sg.Input(key="-AIRLINE-", size=(20,1), default_text="Thai Airways")],
        [sg.Text("Exchange date", size=(12,1)), sg.Input(key="-DATE-", size=(12,1), default_text=datetime.now().strftime("%Y-%m-%d")), sg.Text("YYYY-MM-DD")],
        [sg.Button("Calculate", key="-CALC-", bind_return_key=True), sg.Button("Reset"), sg.Push(), sg.Button("Quit")],
        [sg.HorizontalSeparator()],
        [sg.Text("Results")],
        [sg.Multiline("", key="-RESULT-", size=(90,14), disabled=True, autoscroll=True)],
    ]

    settings_col = [
        [sg.Text("Programs (expiry months & default future ratio)")],
        [sg.Table(
            values=[[name, settings["programs"][name].get("validity_months", 36), settings["programs"][name].get("ratio_multiplier", 1.0)] for name in programs],
            headings=["Program", "Validity (months)", "Default ratio ×"],
            auto_size_columns=False,
            col_widths=[28, 16, 16],
            justification="left",
            key="-PROG_TABLE-",
            enable_events=True,
            num_rows=min(10, len(programs)) or 5,
        )],
        [sg.Text("Selected Program:"), sg.Input(key="-EDIT_NAME-", size=(28,1), disabled=True)],
        [sg.Text("Validity (months)"), sg.Input(key="-EDIT_VALID-", size=(10,1))],
        [sg.Text("Default ratio ×"), sg.Input(key="-EDIT_RATIO-", size=(10,1))],
        [sg.Button("Apply Change"), sg.Push(), sg.Button("Save Settings")],
    ]

    layout = [
        [sg.TabGroup([[sg.Tab("Calculator", calc_col), sg.Tab("Settings", settings_col)]], expand_x=True, expand_y=True)],
        [sg.StatusBar("Ready", key="-STATUS-")]
    ]
    return layout

# Important CAL ------------------------------
def calculate(settings: Dict[str, Any], values: Dict[str, Any]) -> str:
    programs = settings["programs"]
    airports = settings["airports"]

    program = values["-PROGRAM-"]
    cabin = values["-CABIN-"]
    pax = int(values["-PAX-"])
    bonus_pct = float(values.get("-BONUS-", "0") or 0)
    ratio_input = float(values.get("-RATIO-", "1.00") or 1.0)
    airline = (values.get("-AIRLINE-", "") or "").strip()
    use_dist = values["-USE_DIST-"]
    miles_manual = values["-MILES_MANUAL-"].strip()
    exchange_date_str = values["-DATE-"]
    
    # Input validation
    if not program:
        return "Please select a program."
    
    try:
        dt = datetime.strptime(exchange_date_str, "%Y-%m-%d")
    except ValueError:
        return "Exchange date must be YYYY-MM-DD."

    # Determine miles per person based on user choice
    base_per_person = 0
    source = ""

    if use_dist:
        origin_iata = values.get("-ORIGIN-")
        dest_iata = values.get("-DEST-")
        origin = airports.get(origin_iata)
        dest = airports.get(dest_iata)
        if not (origin and dest):
            return "Please choose valid origin/destination IATA codes."
        
        # Priority 1: Check for fixed Business Class override
        if cabin == "Business":
            fixed_miles = override_business_miles(program, dest["iata"])
            if fixed_miles is not None:
                base_per_person = fixed_miles
                source = f"Fixed Business Class override for {program} ({find_dest_group(dest['iata'])})"
            
        # Priority 2: Fallback to distance-based band calculation
        if base_per_person == 0:
            dist = haversine_miles(origin, dest)
            is_own_airline = (airline.lower() == programs[program].get("homeAirline", "").lower())
            
            bands = programs[program]["own"] if is_own_airline else programs[program]["partner"]
            Y, J = band_price(bands, dist)
            base_per_person = J if cabin == "Business" else Y
            
            source = (
                f"Distance-based estimate: {origin['iata']}→{dest['iata']} "
                f"~ {int(round(dist)):,} mi; {'own' if is_own_airline else 'partner'} chart"
            )
            
    else:  # Manual miles entered
        if not miles_manual:
            return "Enter 'miles per person' or enable distance-based estimate."
        try:
            base_per_person = int(miles_manual.replace(",", "").strip())
        except ValueError:
            return "Miles per person must be a number."
        source = "Manual miles per person"

    # All calculations now proceed from a single, determined `base_per_person` value.
    prog = programs[program]
    final_ratio = (float(prog.get("ratio_multiplier", 1.0))) * (ratio_input if ratio_input > 0 else 1.0)
    validity_months = int(prog.get("validity_months", 36))
    
    # Apply future ratio (increase)
    adj_per_person = math.ceil(base_per_person * final_ratio)
    
    # Transfer bonus (points→miles): need fewer points with a bonus
    bonus_factor = 1.0 + (bonus_pct / 100.0) if bonus_pct > 0 else 1.0
    points_needed_per_person = math.ceil(adj_per_person / bonus_factor)
    
    total_miles = adj_per_person * pax
    total_points = points_needed_per_person * pax
    
    # Calculate expiry date
    expiry_dt = add_months(dt, validity_months)
    expiry_str = expiry_dt.strftime("%Y-%m-%d")

    # Format output
    lines = [
        f"Program: {program}   Cabin: {cabin}   Passengers: {pax}",
        f"Airline: {airline or '(unspecified)'}   Future ratio ×: {final_ratio:.2f}",
        source,
        "",
        f"Miles per person (after ratio): {adj_per_person:,}",
        f"Transfer bonus: +{bonus_pct:.0f}% → Points per person needed: {points_needed_per_person:,}" if bonus_pct > 0 else f"Points per person needed: {points_needed_per_person:,}",
        "",
        f"TOTAL miles:  {total_miles:,}",
        f"TOTAL points: {total_points:,}",
        "",
        f"Exchange date: {exchange_date_str} → Expiry in {validity_months} months: {expiry_str}",
        "(Note: real expiry rules can be more complex. You can change validity in Settings.)"
    ]
    
    return "\n".join(lines)

def build_window(settings: Dict[str, Any]):
    layout = build_layout(settings)
    return sg.Window(APP_NAME, layout, resizable=True, finalize=True)

def main():
    settings = load_settings()
    window = build_window(settings)

    # Preselect first row in settings table
    if settings["programs"]:
        window["-PROG_TABLE-"].update(select_rows=[0])
        first = sorted(settings["programs"].keys())[0]
        window["-EDIT_NAME-"].update(first)
        window["-EDIT_VALID-"].update(str(settings["programs"][first].get("validity_months", 36)))
        window["-EDIT_RATIO-"].update(str(settings["programs"][first].get("ratio_multiplier", 1.0)))

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Quit"):
            break

        if event == "Reset":
            window["-BONUS-"].update("0")
            window["-RATIO-"].update("1.00")
            window["-PAX-"].update(1)
            window["-MILES_MANUAL-"].update("")
            window["-RESULT-"].update("")
            window["-STATUS-"].update("Reset complete.")

        if event == "-CALC-":
            result = calculate(settings, values)
            window["-RESULT-"].update(result)
            window["-STATUS-"].update("Calculated.")

        if event == "-PROG_TABLE-":
            try:
                selected = values["-PROG_TABLE-"][0]
                name = sorted(settings["programs"].keys())[selected]
                prog = settings["programs"][name]
                window["-EDIT_NAME-"].update(name)
                window["-EDIT_VALID-"].update(str(prog.get("validity_months", 36)))
                window["-EDIT_RATIO-"].update(str(prog.get("ratio_multiplier", 1.0)))
            except Exception:
                pass

        if event == "Apply Change":
            name = values["-EDIT_NAME-"]
            if not name or name not in settings["programs"]:
                sg.popup_error("Select a program first from the table.")
                continue
            try:
                valid = int(values["-EDIT_VALID-"])
                ratio = float(values["-EDIT_RATIO-"])
            except ValueError:
                sg.popup_error("Validity must be integer months; ratio must be a number.")
                continue
            settings["programs"][name]["validity_months"] = valid
            settings["programs"][name]["ratio_multiplier"] = ratio
            rows = [[n, settings["programs"][n].get("validity_months", 36), settings["programs"][n].get("ratio_multiplier", 1.0)] for n in sorted(settings["programs"].keys())]
            window["-PROG_TABLE-"].update(values=rows)
            window["-STATUS-"].update(f"Updated {name}.")

        if event == "Save Settings":
            save_settings(settings)
            window["-STATUS-"].update("Settings saved to settings.json.")

    window.close()

if __name__ == "__main__":
    main()
