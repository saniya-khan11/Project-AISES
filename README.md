# AISES

## AI Software Evaluation System

### An AI-powered system for evaluating software requirement compliance between Software Requirements Specifications (SRS) and source code.

---

## Overview

AISES (AI Software Evaluation System) is an AI-powered software engineering system that automates the evaluation of software requirement compliance by comparing a Software Requirements Specification (SRS) with the corresponding source code.

The system combines Large Language Models (Google Gemini), Tree-sitter, and static code analysis to extract software requirements, parse source code, map requirements to implementation, evaluate compliance, validate the results, and generate a professional PDF report.

Unlike a single-prompt LLM approach, AISES follows a modular pipeline that improves traceability, scalability, debugging, validation, and maintainability through intermediate processing stages.

---

# Objectives

- Automate software requirement compliance evaluation.
- Reduce manual verification effort.
- Improve software requirement traceability.
- Generate detailed implementation reports.
- Calculate software compliance metrics.
- Demonstrate the application of Artificial Intelligence in Software Engineering.

---

# Key Features

- Automated Requirement Extraction
- Acceptance Criteria Generation
- Tree-sitter Based Source Code Parsing
- Requirement-to-Code Mapping
- AI-assisted Requirement Evaluation
- Mapping Validation
- Evaluation Validation
- Compliance Calculation
- Professional PDF Report Generation
- Intermediate JSON Outputs
- Resume Capability
- Modular Pipeline Architecture

---

# Technologies Used

- Python
- Google Gemini API
- Tree-sitter
- ReportLab
- JSON
- Tkinter (Demonstration Project)

---

# Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/<your-username>/AISES.git
cd AISES
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API

Create a Gemini API Key from Google AI Studio.

Set the environment variable.

### Windows

```cmd
setx GEMINI_API_KEY "YOUR_API_KEY"
```

Restart the terminal.

Verify:

```bash
python -c "import os; print(os.getenv('GEMINI_API_KEY'))"
```

---

## Configure the Model

Edit:

```
app/config/config.json
```

Example:

```json
{
    "gemini_model": "gemini-3.6-flash",
    "gemini_temperature": 0.1,
    "gemini_max_output_tokens": 8192
}
```

---

## Prepare Input Files

Place the SRS inside:

```
examples/sample_srs.txt
```

Place the source code inside:

```
examples/sample_project/
```

---

## Run the Project

```bash
python run.py
```

---

# Example Demonstration

The demonstration project contains:

- Python Calculator SRS
- Python Calculator Source Code

The source code intentionally omits explicit division-by-zero validation to demonstrate AISES's ability to detect missing software requirements.

Example Report:

| Metric | Value |
|---------|------:|
| Total Requirements | 12 |
| Implemented | 11 |
| Partially Implemented | 0 |
| Not Implemented | 1 |
| Overall Compliance | 91.67% |

---

# Advantages

- Requirement-level Traceability
- Modular Pipeline Architecture
- Reduced Manual Review Effort
- AI-assisted Software Evaluation
- Intermediate Outputs for Debugging
- Professional PDF Reporting
- Scalable Architecture
- Resume Capability
- Easy Future Integration

---

# Author

**Saniya Khan**

Project: **AISES – AI Software Evaluation System**

---

# Acknowledgements

AISES leverages **Google Gemini** for semantic analysis and **Tree-sitter** for structural source code parsing to automate software requirement compliance evaluation between Software Requirements Specifications (SRS) and source code.
