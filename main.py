import subprocess
import time
from config.settings import DAY_BEHIND
from core.sla_monitor import SLAMonitor
from utils.helpers import Helper


class MonitorApp:

    def __init__(self):
        self.monitor = SLAMonitor()
        self.last_sla_hour = None

    def run(self):
        subprocess.Popen(["caffeinate", "-dimsu"])

        while True:
            now = Helper.now()
            print(f"BIZDATE: {Helper.format_date_yyyymmdd(Helper.get_prev_day(DAY_BEHIND))}")

            try:
                # Pause monitoring window 23:30 - 00:30
                if (now.hour == 23 and now.minute >= 30) or (now.hour == 0 and now.minute < 30):
                    print(f"[{now.strftime('%H:%M:%S')}] Paused monitoring window")
                    time.sleep(60)
                    continue

                self.monitor.update_sheet_status()

                # SLA check: notify once per hour
                if self.last_sla_hour != now.hour:
                    print(f"Checking SLA at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                    self.monitor.check_sla()
                    self.last_sla_hour = now.hour

            except Exception as e:
                print("Cycle error:", e)

            time.sleep(600)


if __name__ == "__main__":
    app = MonitorApp()
    app.run()