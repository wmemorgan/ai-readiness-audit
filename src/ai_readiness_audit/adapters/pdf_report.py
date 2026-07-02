"""A dependency-free PDF renderer for a ReadinessReport.

Produces a valid single-stream PDF with no third-party dependencies, so the open-source
engine carries no heavy rendering library. It renders a compact text summary; a hosted
deployment may swap in a richer branded PDF adapter behind the same port.
"""

from __future__ import annotations

from ..domain.models import ReadinessReport


class PdfReportRenderer:
    """Implements the PdfRenderer port."""

    def render(self, report: ReadinessReport) -> bytes:
        return _build_pdf(_report_lines(report))


def _report_lines(report: ReadinessReport) -> list[str]:
    lines = [
        "The AI-Readiness Standard — Readiness Report",
        "",
        report.advisory_notice,
        "",
        f"Overall readiness: {report.overall_band.title} ({report.overall_band.name})",
        report.verdict,
        "",
        "By dimension:",
    ]
    for result in report.dimension_results:
        lines.append(f"  - {result.dimension.name}: {result.band.title} ({result.band.name})")
    lines.append("")
    lines.append("Prioritized remediation:")
    for index, gap in enumerate(report.prioritized_remediation, start=1):
        lines.append(f"  {index}. {gap.dimension_name}: {gap.prompt}")
    lines.append("")
    lines.append(report.routing_cta)
    return lines


def _escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _content_stream(lines: list[str]) -> bytes:
    body = ["BT", "/F1 11 Tf", "14 TL", "72 720 Td"]
    for line in lines:
        body.append(f"({_escape(line)}) Tj")
        body.append("T*")
    body.append("ET")
    return "\n".join(body).encode("latin-1", "replace")


def _build_pdf(lines: list[str]) -> bytes:
    content = _content_stream(lines)
    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n".encode() + obj + b"\nendobj\n"

    xref_start = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        b"trailer\n<< /Size "
        + str(len(objects) + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_start).encode()
        + b"\n%%EOF\n"
    )
    return bytes(out)
