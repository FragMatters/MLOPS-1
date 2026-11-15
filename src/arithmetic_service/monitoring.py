"""Evidently AI data monitoring and quality reporting pipeline."""

import json
from pathlib import Path
from typing import Optional, Tuple
import numpy as np
import pandas as pd

# Compatibility shim for pandas 3+ and evidently 0.4+
try:
    import pandas.core.dtypes.common as _c
    if not hasattr(_c, "infer_dtype_from_object"):
        _c.infer_dtype_from_object = lambda x: getattr(x, "dtype", type(x))
except ImportError:
    pass

try:
    from evidently.legacy.report import Report
    from evidently.legacy.metric_preset import DataQualityPreset, DataDriftPreset
except ImportError:
    from evidently.report import Report  # type: ignore
    from evidently.metric_preset import DataQualityPreset, DataDriftPreset  # type: ignore

from arithmetic_service import core

DEFAULT_REPORTS_DIR = Path("reports")
DEFAULT_LOG_PATH = DEFAULT_REPORTS_DIR / "transactions.jsonl"
DEFAULT_HTML_PATH = DEFAULT_REPORTS_DIR / "data_quality_report.html"
DEFAULT_JSON_PATH = DEFAULT_REPORTS_DIR / "data_quality_report.json"


def log_transaction(
    operation: str,
    a: float,
    b: float,
    result: float,
    filepath: Path = DEFAULT_LOG_PATH,
) -> None:
    """Log an arithmetic transaction to a JSONL file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "operation": operation,
        "a": float(a),
        "b": float(b),
        "result": float(result),
    }
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def generate_synthetic_data(n_samples: int = 100, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic arithmetic calculation data across all operations."""
    rng = np.random.default_rng(seed)
    operations = ["add", "subtract", "multiply", "divide"]
    records = []

    for _ in range(n_samples):
        op = rng.choice(operations)
        a = float(rng.uniform(-50.0, 50.0))
        # Ensure denominator isn't 0 for division
        b = float(rng.uniform(0.1, 50.0)) if op == "divide" else float(rng.uniform(-50.0, 50.0))

        if op == "add":
            res = core.add(a, b)
        elif op == "subtract":
            res = core.subtract(a, b)
        elif op == "multiply":
            res = core.multiply(a, b)
        else:
            res = core.divide(a, b)

        records.append({"operation": op, "a": round(a, 4), "b": round(b, 4), "result": round(float(res), 4)})

    return pd.DataFrame(records)


def load_or_generate_datasets(
    log_path: Path = DEFAULT_LOG_PATH,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load logged transactions or generate synthetic reference and current datasets."""
    reference_df = generate_synthetic_data(n_samples=150, seed=42)

    log_file = Path(log_path)
    if log_file.exists() and log_file.stat().st_size > 0:
        lines = [json.loads(line) for line in log_file.read_text(encoding="utf-8").strip().splitlines() if line.strip()]
        if len(lines) >= 10:
            current_df = pd.DataFrame(lines)
            return reference_df, current_df

    # Fallback to current synthetic distribution
    current_df = generate_synthetic_data(n_samples=150, seed=123)
    return reference_df, current_df


def generate_monitoring_report(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    html_path: Path = DEFAULT_HTML_PATH,
    json_path: Path = DEFAULT_JSON_PATH,
) -> Tuple[Path, Path]:
    """Execute Evidently report evaluation and write HTML and JSON artifacts."""
    html_path = Path(html_path)
    json_path = Path(json_path)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    report = Report(metrics=[DataQualityPreset(), DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)

    report.save_html(str(html_path))
    report.save_json(str(json_path))

    return html_path, json_path


def main() -> None:
    """Entrypoint to run Evidently data monitoring pipeline."""
    print("Running Evidently Data Monitoring Pipeline...")
    ref_df, curr_df = load_or_generate_datasets()
    print(f"Loaded datasets - Reference: {len(ref_df)} rows, Current: {len(curr_df)} rows")
    html_out, json_out = generate_monitoring_report(ref_df, curr_df)
    print(f"Report generated successfully!")
    print(f"  - HTML: {html_out}")
    print(f"  - JSON: {json_out}")


if __name__ == "__main__":
    main()
