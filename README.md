# CP Debugger Engine (offline)

**A compiler-aware C++ debugging engine integrating native compilation analysis with CUDA-accelerated local LLM inference.**

## Overview
`CP Debugger Engine` is a hybrid systems project that combines traditional compilation workflows with modern AI-assisted reasoning.
Instead of blindly sending code to a language model, the system first performs a real `g++` compilation check and then intelligently routes the task to a locally hosted DeepSeek-Coder model running on a CUDA-accelerated `llama.cpp` backend.
The entire pipeline runs locally without relying on external APIs or cloud-based inference services.

This project demonstrates:

- Systems design
- Compiler integration
- Local LLM infrastructure
- Backend engineering
- Deterministic inference workflows

## Key Features
- Real C++ compilation using `g++`
- Logical analysis via DeepSeek-Coder (6.7B)
- Optional full corrected code generation
- CUDA-accelerated inference using llama.cpp
- Fully offline execution
- Deterministic responses (`temperature = 0.0`)
- Regex-based output sanitization

## Supported Interfaces

`CP Debugger Engine` currently supports:

- Browser-based debugging interface
- REST API backend
- Command-line interface (CLI)

This allows the project to function both as a local web application and as a terminal-based developer utility.

## System Architecture
```
Browser UI
     |
     v
Flask Backend (Orchestrator)
     |
     |-- Compilation Layer (g++)
     |        |
     |        |-- Compiler Errors
     |
     |-- LLM Inference Layer
              |
              |-- llama-server (CUDA)
                     |
                     |-- DeepSeek-Coder 6.7B
                             |
                             v
                     Output Sanitization
                             |
                             v
                         JSON Response
```

Detailed architecture documentation:

```text
docs/architecture.md
```

## Project Structure
```
cp-debugger-engine/
│
├── backend/
│   ├── app.py
│   ├── cli.py
│   ├── requirements.txt
│
├── frontend/
│   └── templates/
│       └── index.html
│
├── examples/
│   └── test.cpp
│
├── docs/
│   ├── architecture.md
│   └── installation.md
│
├── README.md
├── .gitignore
└── venv/
```

## CLI Usage

Analyze code:

```bash
python cli.py ../examples/test.cpp
```

Generate corrected code:

```bash
python cli.py ../examples/test.cpp --fix
```

## Installation

Full installation guide available in:

```text
docs/installation.md
```

## Technologies Used

### Backend

- Python
- Flask
- requests
- subprocess
- tempfile
- regex (`re`)

### AI Stack

- llama.cpp
- DeepSeek-Coder 6.7B
- CUDA Toolkit 12.4

### Frontend

- HTML
- CSS
- JavaScript

### Build Tools

- CMake
- Ninja
- Visual Studio 2022 Build Tools

## Why This Project Matters

This project demonstrates:

- Compiler integration
- Local LLM serving infrastructure
- CUDA acceleration
- Deterministic inference control
- Structured prompt routing
- Developer tooling workflows
- Hybrid systems + AI architecture

It combines:

- Systems Programming
- AI Infrastructure
- Backend Engineering
- Developer Tooling

## How It Works
1. User submits C++ code
2. Backend compiles using g++
3. If compilation fails:
```
-Analysis mode → return compiler errors
-Fix mode → send errors to LLM
```
4. LLM runs locally via CUDA
5. Output is cleaned using regex
6. Clean JSON response returned

