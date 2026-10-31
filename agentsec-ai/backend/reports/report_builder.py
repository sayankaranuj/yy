"""Build structured report artifacts for AgentSec AI."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from backend.reports.owasp_mapper import map_severity_to_owasp
from backend.storage import FindingsStore
from backend.utils.redaction import redact_mapping


def _report_filename_stem(target: str) -> str:
    """Convert a target into a filename stem that is valid on Windows and Unix."""

    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", target).rstrip(" .")
    if not stem:
        stem = "report"
    if stem.split(".", maxsplit=1)[0].upper() in {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }:
        stem = f"_{stem}"
    return stem


def build_report_artifacts(
    target: str,
    findings: list[dict[str, Any]] | None = None,
    scan_id: int | str | None = None,
) -> list[dict[str, Any]]:
    """Create markdown and JSON report artifacts for a target."""

    if findings is None:
        findings = FindingsStore().list_records()
    findings = [redact_mapping(finding) for finding in findings]
    markdown_lines = [
        f"# AgentSec AI Report for {target}",
        "",
        "## Summary",
        f"- Target: {target}",
        *([f"- Scan ID: {scan_id}"] if scan_id is not None else []),
        f"- Findings: {len(findings)}",
        "",
        "## Findings",
    ]

    for finding in findings:
        markdown_lines.append(
            f"- {finding.get('title', 'Finding')} [{finding.get('severity', 'info')}]"
        )
        if finding.get("affected_url"):
            markdown_lines.append(f"  - Location: {finding['affected_url']}")
        if finding.get("description"):
            markdown_lines.append(f"  - Details: {finding['description']}")
        if finding.get("evidence"):
            markdown_lines.append(
                f"  - Evidence: {json.dumps(finding['evidence'], ensure_ascii=False)}"
            )

    markdown_content = "\n".join(markdown_lines)
    json_payload = {
        "target": target,
        "scan_id": scan_id,
        "findings": [
            {
                **finding,
                "title": finding.get("title", "Finding"),
                "severity": finding.get("severity", "info"),
                "status": finding.get("status", "open"),
                "owasp": map_severity_to_owasp(finding.get("severity", "info")),
            }
            for finding in findings
        ],
    }

    report_dir = Path(__file__).resolve().parent / "generated"
    report_dir.mkdir(parents=True, exist_ok=True)

    filename_stem = _report_filename_stem(target)
    if scan_id is not None:
        filename_stem = f"{filename_stem}-scan-{scan_id}"
    markdown_path = report_dir / f"{filename_stem}.md"
    json_path = report_dir / f"{filename_stem}.json"
    markdown_path.write_text(markdown_content, encoding="utf-8")
    json_path.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    return [
        {"format": "markdown", "name": markdown_path.name, "path": str(markdown_path)},
        {"format": "json", "name": json_path.name, "path": str(json_path)},
    ]


def build_pdf_artifact(
    target: str,
    findings: list[dict[str, Any]],
    scan_id: int | str | None = None,
    detail: dict[str, Any] | None = None,
) -> Path:
    """Render a redacted scan report as a PDF artifact."""

    from weasyprint import HTML

    safe_findings = [redact_mapping(finding) for finding in findings]
    detail = detail or {}
    rows = "".join(
        f"<article><h2>{finding.get('title', 'Finding')} "
        f"<span>{finding.get('severity', 'info').upper()}</span></h2>"
        f"<p>{finding.get('description') or 'No description provided.'}</p>"
        f"<p><b>Location:</b> {finding.get('affected_url') or 'Not specified'}</p>"
        f"<p><b>Confidence:</b> {finding.get('confidence', 'Not provided')}</p>"
        f"<p><b>Reproduction:</b> {finding.get('reproduction_steps', 'Review the evidence below against the affected asset.')}</p>"
        f"<p><b>Remediation:</b> {finding.get('remediation', 'Apply the vendor or technology-specific hardening guidance and retest.')}</p>"
        f"<p><b>CWE:</b> {finding.get('cwe', 'Not mapped')} &nbsp; <b>OWASP:</b> {finding.get('owasp_category', 'Not mapped')}</p>"
        f"<pre>{json.dumps(finding.get('evidence'), indent=2, default=str)}</pre></article>"
        for finding in safe_findings
    )
    summary = detail.get("executive_summary", {})
    timeline = detail.get("timeline", {})
    failed = detail.get("failed_checks", [])
    skipped = detail.get("skipped_checks", [])
    stages = "".join(
        f"<li>{stage.get('name')}: {stage.get('status')} ({stage.get('duration_ms') or 0} ms)</li>"
        for stage in timeline.get("stages", [])
    )
    checks = "".join(
        f"<li>{step.get('task_name')}: {step.get('status')}</li>"
        for step in [*failed, *skipped]
    )
    html = f"""<!doctype html><html><head><meta charset="utf-8">
    <style>body{{font-family:Arial,sans-serif;color:#17202a}}h1{{color:#9b1c1c}}
    h2{{border-bottom:1px solid #ddd;padding-bottom:6px}}h2 span{{font-size:12px}}
    article{{page-break-inside:avoid;margin:20px 0}}pre{{white-space:pre-wrap;background:#f4f4f4;padding:10px}}
    </style></head><body><h1>AgentSec AI Security Report</h1>
    <p><b>Target:</b> {target}</p>
    <p><b>Scan ID:</b> {scan_id if scan_id is not None else 'N/A'}</p>
    <h2>Executive summary</h2><p>{summary.get('headline', 'No summary available.')}</p>
    <p><b>Coverage:</b> {summary.get('coverage', 'Not available')}</p>
    <h2>Stage timeline</h2><ul>{stages or '<li>No stage timing was persisted.</li>'}</ul>
    <h2>Failed and skipped checks</h2><ul>{checks or '<li>None recorded.</li>'}</ul>
    <h2>Findings ({len(safe_findings)})</h2>{rows or '<p>No findings were recorded.</p>'}
    </body></html>"""
    report_dir = Path(__file__).resolve().parent / "generated"
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = _report_filename_stem(target)
    if scan_id is not None:
        stem = f"{stem}-scan-{scan_id}"
    path = report_dir / f"{stem}.pdf"
    HTML(string=html).write_pdf(str(path))
    return path
