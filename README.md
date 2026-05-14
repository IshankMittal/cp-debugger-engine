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

## Full Windows Installation Guide

### 1. Install Python `(3.10+)`
Download from: https://www.python.org/downloads/windows/

During installation: Check Add Python to PATH & Select Install for all users

Verify:
```
python --version
```
Expected:
```
Python 3.10+
```

### 2. Install Git
Download from: https://git-scm.com/download/win

During installation: Keep default options & Select Git from command line and also from 3rd-party software

Verify:
```
git --version
```

### 3. Install CMake
Download from: https://cmake.org/download/ (Choose Windows x64 Installer (.msi))

During installation: Check Add CMake to system PATH

Verify:
```
cmake --version
```

### 4. Install Ninja
Open PowerShell:
```
winget install Ninja-build.Ninja
```
Verify:
```
ninja --version
```

### 5. Install Visual Studio 2022 Build Tools
Download from: https://visualstudio.microsoft.com/downloads/

Download: Build Tools for Visual Studio 2022

Ensure:
- MSVC v143 C++ x64/x86 build tools
- Windows 10/11 SDK
- C++ CMake tools

Verify:
```
Open x64 Native Tools Command Prompt for VS 2022
```

Run:
```
cl
```

### 6. Install NVIDIA GPU Driver
Download from: https://www.nvidia.com/Download/index.aspx

Verify:
```
nvidia-smi
```

### 7. Install CUDA Toolkit (12.4 Recommended)
Download from: https://developer.nvidia.com/cuda-downloads

Verify:
```
nvcc --version
```

Expected:
```
Cuda compilation tools, release 12.4
```

## Setup llama.cpp
### 1. Clone llama.cpp
```
cd C:\
mkdir llm
cd llm
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

### 2. Build llama.cpp (CUDA + Release)
Use x64 Native Tools Command Prompt for VS 2022

```
cmake -B build -G Ninja -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

This builds:
- `llama-server.exe`
- CUDA backend

### 3. Download DeepSeek Model
Download: `deepseek-coder-6.7b-instruct-q4_k_m.gguf`

Place it in:
```
C:\llm\models\
```

## Start LLM Server
```
cd C:\llm\llama.cpp\build\bin
```

Run:
```
.\llama-server.exe -m "C:\llm\models\deepseek-coder-6.7b-instruct-q4_k_m.gguf" -ngl 18 -c 4096 -t 6 --port 8080 -n 256
```

If successful:
```
http://localhost:8080
```

## Setup CP Debugger Engine
Clone your repository:
```
git clone https://github.com/IshankMittal/cp-debugger-engine.git
cd cp-debugger-engine
```

Create virtual environment:
```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```
pip install -r backend/requirements.txt
```

## Start Backend
```
python backend/app.py
```

Open:
```
http://127.0.0.1:5000
```

## CLI Mode

The project also includes a command-line interface for direct terminal usage.

Example:

```bash
python cli.py test.cpp
```

Auto-fix mode:

```
python cli.py test.cpp --fix
```

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
│
├── README.md
├── .gitignore
└── venv/
```
