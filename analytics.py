from pathlib import Path
import pandas as pd


class SessionAnalytics:
    """Saves session logs to CSV and computes summary metrics."""

    def __init__(self, log_dir: str = "data/logs"):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.csv_file = self.log_path / "session_logs.csv"

    def save_records(self, records: list[dict]) -> Path:
        if not records:
            return self.csv_file

        df_new = pd.DataFrame(records)
        if self.csv_file.exists():
            df_old = pd.read_csv(self.csv_file)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(self.csv_file, index=False)
        return self.csv_file

    def summarize(self, records: list[dict]) -> dict:
        if not records:
            return {
                "total_snapshots": 0,
                "avg_engagement": 0.0,
                "max_engagement": 0.0,
                "min_engagement": 0.0,
                "latest_attendance": "Observing",
            }

        df = pd.DataFrame(records)
        return {
            "total_snapshots": int(len(df)),
            "avg_engagement": round(float(df["overall_engagement"].mean()), 1),
            "max_engagement": round(float(df["overall_engagement"].max()), 1),
            "min_engagement": round(float(df["overall_engagement"].min()), 1),
            "latest_attendance": str(df["attendance_status"].iloc[-1]),
        }