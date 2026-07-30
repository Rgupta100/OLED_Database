# OLED Database

Raspberry Pi system-stats logger. Collects IP, CPU temperature, CPU usage, RAM,
free disk and Wi-Fi SSID, shows them on an SSD1306 OLED, and persists every
sample to SQLite through SQLAlchemy.

Unlike [`Pi-OLED-Dashboard`](https://github.com/Rgupta100/Pi-OLED-Dashboard),
this version **keeps history** and **degrades to the terminal** when no display
is attached, so it runs on any machine.

## Schema

`Database.py` defines one table via the SQLAlchemy declarative ORM:

```
system_stats
  id            INTEGER  primary key, autoincrement
  ip_address    STRING   not null
  temperature   FLOAT    not null
  cpu_usage     FLOAT    not null
  ram_used_mb   INTEGER  not null
  disk_free_gb  FLOAT    not null
  wifi_ssid     STRING   nullable
  timestamp     DATETIME server default now()
```

`timestamp` is filled by the database with `func.now()`, not by Python — so the
time recorded is the insert time and doesn't drift with application clock
handling.

Database file: `pi_stats.db` in the working directory.

## Setup

```bash
pip3 install -r requirements.txt
python3 Database.py      # creates the table — run once
python3 Main.py          # start collecting
```

`Database.py` is idempotent: `create_all` skips tables that already exist.

### Hardware (optional)

SSD1306 OLED on I²C bus 1, address 0x3C — same wiring as `Pi-OLED-Dashboard`.
Without it, the script prints to stdout every 2 s instead.

## Behaviour

- With a display: renders six rows, refreshing at 1 Hz.
- Above 70 °C or below 10 °C: a full-screen `Temp Too HIGH` / `Temp Too LOW`
  warning flashes three times in place of the normal view.
- Without a display: prints a `--- System Stats ---` block every 2 s.

## Notes and limitations

- **`Main.py` and `Oled_Screen_Display.py` are byte-identical duplicates.** Only
  one is needed; the other should be deleted.
- Nothing prunes the database. At 1 Hz this grows without limit — add a
  retention policy or a longer sample interval before leaving it running.
- Every sample is its own `INSERT` with no batching, so the SD card takes a
  write per second. That's hard on flash over time.
- The Wi-Fi SSID comes from parsing `iwconfig wlan0` and inherits the same
  fragility described in `Pi-OLED-Dashboard` — wrong interface name, Ethernet,
  or a localised system all break it.
- No index on `timestamp`, so range queries scan the table.

## Files

```
Main.py                  collector + display loop
Oled_Screen_Display.py   duplicate of Main.py
Database.py              SQLAlchemy model + table creation
requirements.txt
```
