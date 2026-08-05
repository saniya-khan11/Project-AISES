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

# System Architecture

```text
                   Software Requirements Specification
                                   │
                                   ▼
                      Requirement Generator
                                   │
                          requirements.json
                                   │
                                   ▼
                        Tree-sitter Parser
                                   │
                          project_cst.json
                                   │
                                   ▼
                     Candidate Retriever
                                   │
                     candidate_cst.json
                                   │
                                   ▼
                      Requirement Mapper
                                   │
                            mapping.json
                                   │
                                   ▼
                       Mapping Validator
                                   │
                  validated_mapping.json
                                   │
                                   ▼
                    Requirement Evaluator
                                   │
                          evaluation.json
                                   │
                                   ▼
                    Evaluation Validator
                                   │
               validated_evaluation.json
                                   │
                                   ▼
                   Compliance Calculator
                                   │
                 compliance_summary.json
                                   │
                                   ▼
                    PDF Report Generator
                                   │
                       AISES_Report.pdf
```

---

# Project Workflow

## Phase 1 – Requirement Processing

### Module

Requirement Generator

### Input

```
sample_srs.txt
```

### Output

```
requirements.json
```

### Description

Processes the Software Requirements Specification using Google Gemini and converts the document into structured software requirements and acceptance criteria.

---

## Phase 2 – Source Code Parsing

### Modules

- Project Loader
- Tree-sitter Parser

### Input

```
Source Code Project
```

### Output

```
project_cst.json
```

### Description

Loads every supported source file and generates its Concrete Syntax Tree (CST) while preserving the original source code.

---

## Phase 3 – Candidate Retrieval

### Module

Candidate Retriever

### Input

```
requirements.json
project_cst.json
```

### Output

```
candidate_cst.json
```

### Description

Retrieves only the most relevant source files for each acceptance criterion, reducing unnecessary processing and optimizing search space for the LLM to be used in the next module.

---

## Phase 4 – Requirement Mapping

### Module

Requirement Mapper

### Input

```
requirements.json
candidate_cst.json
```

### Output

```
mapping.json
```

### Description

Maps every acceptance criterion to the most relevant source files, functions, and code structures.

---

## Phase 5 – Mapping Validation

### Module

Mapping Validator

### Input

```
mapping.json
```

### Output

```
validated_mapping.json
```

### Description

Validates generated mappings and removes inconsistent or invalid mappings before evaluation.

---

## Phase 6 – Requirement Evaluation

### Module

Requirement Evaluator

### Input

```
validated_mapping.json
project_cst.json
```

### Output

```
evaluation.json
```

### Description

Evaluates every acceptance criterion using Google Gemini and determines whether it is:

- Implemented
- Partially Implemented
- Not Implemented

---

## Phase 7 – Evaluation Validation

### Module

Evaluation Validator

### Input

```
evaluation.json
```

### Output

```
validated_evaluation.json
```

### Description

Ensures evaluation consistency by validating AI-generated responses.

---

## Phase 8 – Compliance Calculation

### Module

Compliance Calculator

### Input

```
validated_evaluation.json
```

### Output

```
compliance_summary.json
```

### Description

Calculates:

- Total Requirements
- Implemented Requirements
- Partially Implemented Requirements
- Not Implemented Requirements
- Overall Compliance Percentage

---

## Phase 9 – Report Generation

### Module

PDF Report Generator

### Input

```
Validated Evaluation
Compliance Summary
```

### Output

```
AISES_Report.pdf
```

### Description

Generates a professional software compliance report containing:

- Executive Summary
- Requirement-wise Evaluation
- Coverage
- Confidence
- Matched Files
- Strengths
- Issues
- Recommendations
- Overall Compliance

---

# Generated Outputs

| Output File | Description |
|-------------|-------------|
| requirements.json | Structured requirements extracted from the SRS |
| project_cst.json | Parsed source code and Concrete Syntax Tree |
| candidate_cst.json | Candidate source files for every requirement |
| mapping.json | Requirement-to-code mappings |
| validated_mapping.json | Validated mappings |
| evaluation.json | Requirement evaluation |
| validated_evaluation.json | Validated evaluation |
| compliance_summary.json | Compliance statistics |
| AISES_Report.pdf | Final software evaluation report |

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