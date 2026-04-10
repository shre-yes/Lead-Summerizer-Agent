import csv
import logging
import os
from typing import Optional, List, Dict, Any, Generator

logger = logging.getLogger(__name__)

def is_binary_file(file_path: str) -> bool:
    """Checks if a file appears to be binary (like .xlsx)."""
    try:
        with open(file_path, "rb") as f:
            header = f.read(1024)
            return b"PK\x03\x04" in header or b"\x00" in header
    except (IOError, OSError) as e:
        logger.error(f"Error checking file type for {file_path}: {e}")
        return False

def detect_csv_settings(file_path: str) -> tuple[Optional[str], str]:
    """Detects encoding and delimiter for a CSV file."""
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                sample = f.read(1024)
                if not sample:
                    return enc, ","
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    logger.info(f"Detected encoding: {enc}, delimiter: '{dialect.delimiter}'")
                    return enc, dialect.delimiter
                except Exception:
                    return enc, ","
        except (UnicodeDecodeError, Exception):
            continue
    return None, ","

def read_csv_rows(file_path: str, encoding: str, delimiter: str) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that yields normalized and validated rows from a CSV.
    Refactored to separate reading from processing.
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            
            if not reader.fieldnames:
                return

            # Normalize headers
            original_fields = reader.fieldnames
            reader.fieldnames = [h.strip().lower() for h in original_fields if h]
            expected_cols = len(reader.fieldnames)

            for line_num, row in enumerate(reader, start=2):
                # Check for malformed rows
                if None in row or any(v is None for v in row.values()) or len(row) < expected_cols:
                    logger.warning(f"Skipping malformed row at line {line_num}")
                    continue
                yield row
    except (IOError, csv.Error) as e:
        logger.error(f"Error reading CSV {file_path}: {e}")

def save_results(output_path: str, results: List[Dict[str, Any]]) -> None:
    """Saves specific columns to the output CSV."""
    target_columns = ["name", "company", "note", "email", "phone", "summary"]
    
    try:
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=target_columns, 
                extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(results)
    except (PermissionError, IOError) as e:
        logger.error(f"Failed to save results to {output_path}: {e}")
