# CP Debugger Engine - Installation Guide

## System Requirements

- Windows 10/11
- Python 3.10+
- Git
- CMake
- Ninja
- Visual Studio 2022 Build Tools
- NVIDIA GPU
- CUDA Toolkit 12.4
- Minimum 8GB RAM

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
### 1. Clone your repository:
```
git clone https://github.com/IshankMittal/cp-debugger-engine.git
cd cp-debugger-engine
```

### 2. Create virtual environment:
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies:
```
pip install -r backend/requirements.txt
```

### 4. Start Backend
```
cd backend

python app.py
```

Open:
```
http://127.0.0.1:5000
```

### 5. Run CLI

Example:

```bash
python cli.py ../examples/test.cpp
```

Fix mode:

```bash
python cli.py ../examples/test.cpp --fix
```

### 6. Open Browser UI

Open:

```text
http://127.0.0.1:5000
```
