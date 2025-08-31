# Mileage Calculator – Local Python GUI

A simple **Python GUI app** (using [FreeSimpleGUI](https://github.com/PySimpleGUI/FreeSimpleGUI)) to estimate award miles and points for airline mileage programs.

## ✨ Features
- Adjustable ratio multipliers (simulate future devaluations)
- Transfer bonus (%) support (e.g., 20% promo)
- Exchange date → automatic expiry date (per-program validity months)
- Number of passengers support (totals calculated)
- Distance-based estimate (Haversine from origin/destination airports) **or** manual miles input
- Editable program settings (validity months, default ratio) saved in `settings.json`

## 📂 Project Structure
```
C:\mileage_UOB\
│
├── mileage_gui.py        # Main program
├── run_mileage_gui.bat   # Double-click launcher (sets FreeSimpleGUI path)
├── FreeSimpleGUI-main\   # Local FreeSimpleGUI repo
└── settings.json         # Created automatically to store program settings
```

## 🚀 How to Run
1. **Install Python 3.13** (or newer).
2. Clone/download [FreeSimpleGUI](https://github.com/PySimpleGUI/FreeSimpleGUI) into:
   ```
   C:\mileage_UOB\FreeSimpleGUI-main
   ```
3. Launch the program by double-clicking:
   ```
   run_mileage_gui.bat
   ```

The batch file ensures Python loads **FreeSimpleGUI** instead of the new paid `PySimpleGUI v5`.

---

## 🛠️ Program Usage
- **Calculator Tab**
  - Select **Program** and **Cabin**
  - Set number of **Passengers**
  - Enter optional **Transfer bonus %**
  - Adjust **Future ratio ×** (default 1.00)
  - Choose **Origin** / **Destination** IATA code  
    - or manually input *Miles per person*
  - Enter **Operating Airline**
  - Set **Exchange date** (YYYY-MM-DD) → app shows expiry date
  - Click **Calculate**

- **Settings Tab**
  - View/edit program validity (months) and default ratio
  - Click **Apply Change** then **Save Settings**

---

## ⚠️ Notes
- Default charts are demo values only. Replace them in `mileage_gui.py` → `DEMO_RATE_TABLES`.
- Expiry logic is simplified: fixed validity in months. Real programs may have activity-based rules.
- `settings.json` stores your custom settings so you don’t lose edits between runs.

---

## 🔧 Troubleshooting
- **ModuleNotFoundError: FreeSimpleGUI**  
  Ensure you have `FreeSimpleGUI-main` in the project folder and use `run_mileage_gui.bat` to launch.
- **Accidentally installed paid PySimpleGUI v5**  
  No problem. Just uninstall it:
  ```powershell
  python -m pip uninstall PySimpleGUI -y
  ```
  and always use `FreeSimpleGUI`.

---

## 📜 License
This project is for **personal use only**. FreeSimpleGUI is MIT-licensed.
