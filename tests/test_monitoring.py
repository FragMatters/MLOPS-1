"""Unit tests for Evidently data monitoring module."""

from pathlib import Path
import pandas as pd
from arithmetic_service.monitoring import (
    generate_synthetic_data,
    log_transaction,
    load_or_generate_datasets,
)


def test_synthetic_data_generation():
    df = generate_synthetic_data(n_samples=50, seed=99)
    assert len(df) == 50
    assert list(df.columns) == ["operation", "a", "b", "result"]
    assert set(df["operation"].unique()).issubset({"add", "subtract", "multiply", "divide"})


def test_transaction_logging(tmp_path: Path):
    log_file = tmp_path / "test_tx.jsonl"
    log_transaction("multiply", 4.0, 5.0, 20.0, filepath=log_file)
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert '"operation": "multiply"' in content
    assert '"result": 20.0' in content


def test_load_or_generate_datasets(tmp_path: Path):
    log_file = tmp_path / "empty.jsonl"
    ref_df, curr_df = load_or_generate_datasets(log_path=log_file)
    assert isinstance(ref_df, pd.DataFrame)
    assert isinstance(curr_df, pd.DataFrame)
    assert len(ref_df) > 0
    assert len(curr_df) > 0
