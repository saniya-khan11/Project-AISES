import json
from pathlib import Path


class HTMLReportGenerator:
    """
    Generates a professional HTML report
    from report.json
    """

    def generate(
        self,
        report_json="outputs/report.json",
        output_file="outputs/report.html"
    ):

        with open(report_json, encoding="utf-8") as fp:
            report = json.load(fp)

        summary = report["summary"]

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>AISES Report</title>

<style>

body {{

font-family: Arial;

margin:40px;

background:#f5f5f5;

}}

.container {{

background:white;

padding:30px;

border-radius:8px;

}}

table {{

width:100%;

border-collapse:collapse;

margin-top:20px;

}}

th,td {{

border:1px solid #ddd;

padding:10px;

}}

th {{

background:#1f77b4;

color:white;

}}

.pass {{

color:green;

font-weight:bold;

}}

.partial {{

color:orange;

font-weight:bold;

}}

.fail {{

color:red;

font-weight:bold;

}}

.card {{

display:inline-block;

padding:20px;

margin:10px;

background:#f0f0f0;

border-radius:10px;

min-width:180px;

text-align:center;

}}

</style>

</head>

<body>

<div class="container">

<h1>AISES Software Evaluation Report</h1>

<h2>Executive Summary</h2>

<div class="card">

<h3>Total Requirements</h3>

<p>{summary['total_requirements']}</p>

</div>

<div class="card">

<h3>Implemented</h3>

<p>{summary['implemented']}</p>

</div>

<div class="card">

<h3>Partial</h3>

<p>{summary['partially_implemented']}</p>

</div>

<div class="card">

<h3>Not Implemented</h3>

<p>{summary['not_implemented']}</p>

</div>

<div class="card">

<h3>Compliance</h3>

<p>{summary['overall_compliance']}%</p>

</div>

<h2>Requirement Traceability Matrix</h2>

<table>

<tr>

<th>AC ID</th>

<th>Requirement</th>

<th>Status</th>

<th>Coverage</th>

<th>Confidence</th>

</tr>
"""

        for req in report["requirements"]:

            status = req["status"]

            css = "fail"

            if status == "Implemented":
                css = "pass"

            elif status == "Partially Implemented":
                css = "partial"

            html += f"""

<tr>

<td>{req['ac_id']}</td>

<td>{req['requirement_title']}</td>

<td class="{css}">{status}</td>

<td>{req['coverage']}%</td>

<td>{req['confidence']}</td>

</tr>

"""

        html += """

</table>

</div>

</body>

</html>

"""

        Path(output_file).write_text(
            html,
            encoding="utf-8"
        )

        print(f"Saved : {output_file}")

        return output_file