from __future__ import annotations

import csv
import math
import os
from pathlib import Path
from typing import Any, Iterable, Mapping


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float):
        return math.isnan(value)
    if isinstance(value, str):
        stripped = value.strip()
        return stripped == "" or stripped.lower() in {"nan", "none", "null", "nat"}
    return False


def clean_text(value: Any) -> str:
    if is_missing(value):
        return ""
    return str(value).strip()


def clean_optional_int(value: Any) -> str:
    text = clean_text(value)
    if text == "":
        return ""
    return str(int(float(text)))


def clean_required_int(value: Any, default: int = 0) -> str:
    text = clean_text(value)
    if text == "":
        return str(default)
    return str(int(float(text)))


def clean_optional_float(value: Any) -> str:
    text = clean_text(value)
    if text == "":
        return ""
    number = float(text)
    if math.isnan(number):
        return ""
    return str(number)


def clean_bool_flag(value: Any, default: str = "0") -> str:
    text = clean_text(value)
    if text == "":
        return default
    lowered = text.lower()
    if lowered in {"true", "t", "1", "yes"}:
        return "1"
    if lowered in {"false", "f", "0", "no"}:
        return "0"
    return text


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clear_csv_files(path: str | Path, keep: set[str] | None = None) -> None:
    directory = ensure_directory(path)
    keep = keep or set()
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix.lower() == ".csv" and entry.name not in keep:
            entry.unlink()


def write_csv(path: str | Path, headers: list[str], rows: Iterable[Mapping[str, Any]]) -> None:
    output_path = Path(path)
    ensure_directory(output_path.parent)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            sanitized_row = {header: clean_text(row.get(header, "")) for header in headers}
            writer.writerow(sanitized_row)

