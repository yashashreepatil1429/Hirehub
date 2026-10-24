from __future__ import annotations

import csv
import io
from typing import Any, Dict, List


class ReportService:
    @staticmethod
    def generate_csv(rows: List[Dict[str, Any]], filename: str = 'report.csv') -> str:
        if not rows:
            rows = [{}]
        buffer = io.StringIO()
        fieldnames = sorted({key for row in rows for key in row.keys()})
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, '') for key in fieldnames})
        return buffer.getvalue()
