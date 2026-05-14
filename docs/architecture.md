# CP Debugger Engine - Architecture

## Overview

CP Debugger Engine is a compiler-aware offline debugging system designed for competitive programming and C++ debugging workflows.

The project combines:

- Native compiler validation
- Local LLM inference
- CUDA acceleration
- Backend orchestration
- CLI + browser interfaces

into a single debugging pipeline.

## High-Level Architecture

```text
Browser UI / CLI
        │
        ▼
Flask Backend (Orchestrator)
        │
        ├── g++ Compilation Layer
        │        │
        │        └── Compiler Diagnostics
        │
        └── LLM Inference Layer
                 │
                 └── llama-server (CUDA)
                          │
                          └── DeepSeek-Coder 6.7B
                                   │
                                   ▼
                           Output Sanitization
                                   │
                                   ▼
                              JSON Response
```

## System Components

### 1. Frontend Layer

The frontend provides a lightweight browser-based interface for:

- Pasting C++ code
- Selecting fix mode
- Viewing compiler errors
- Viewing corrected code
- Viewing logical analysis

The frontend is implemented using:

- HTML
- CSS
- JavaScript

### 2. CLI Layer

The project also supports direct command-line usage.

Example:

```bash
python cli.py test.cpp
```

Auto-fix mode:

```bash
python cli.py test.cpp --fix
```

CLI support transforms the project from a browser application into a developer utility.

### 3. Flask Backend

The Flask backend acts as the orchestration layer.

Responsibilities:

- Receive requests
- Handle compiler checks
- Build prompts dynamically
- Communicate with llama-server
- Perform output sanitization
- Return structured JSON responses

Main endpoint:

```text
/debug
```

### 4. Compiler Validation Layer

Before invoking the language model, the system performs real compilation using:

```bash
g++ temp.cpp
```

This provides:

- Real syntax checking
- Accurate compiler diagnostics
- Reduced hallucinated errors
- Deterministic debugging flow

## Decision Flow

### Case 1

Compiler Error + Fix Mode OFF

Result:
- Return compiler diagnostics directly

### Case 2

Compiler Error + Fix Mode ON

Result:
- Send compiler diagnostics to LLM
- Generate corrected code

### Case 3

Valid Compilation + Fix Mode OFF

Result:
- Perform logical analysis
- Discuss edge cases
- Analyze time complexity

### Case 4

Valid Compilation + Fix Mode ON

Result:
- Generate optimized corrected implementation

## LLM Inference Layer

Inference is handled locally using:

- llama.cpp
- CUDA backend
- DeepSeek-Coder 6.7B

The model runs through:

```text
llama-server.exe
```

Benefits:

- Fully offline execution
- No API dependency
- Lower long-term cost
- Better privacy
- Local GPU acceleration

## Why DeepSeek-Coder Was Chosen

DeepSeek-Coder was selected because:

- Strong C++ reasoning capability
- Better debugging quality than CodeLlama
- Good instruction-following behavior
- Small enough for RTX 3050 4GB VRAM
- Good balance between speed and quality

## Output Sanitization

LLM outputs often contained:

- Markdown wrappers
- Extra explanations
- Tags like:
  - `[OUT]`
  - `[ANSWER]`
  - `[RESP]`

Regex-based cleaning was implemented to:

- Extract valid C++ code
- Remove wrappers
- Improve CLI readability
- Return compiler-ready output

## CUDA Acceleration

The project uses CUDA acceleration through llama.cpp.

Build configuration:

```bash
cmake -B build -G Ninja -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
```

Benefits:

- Faster inference
- Better GPU utilization
- Reduced response latency

## Current Limitations

Current limitations include:

- No runtime execution sandbox
- No streaming token generation
- Limited by 4GB VRAM
- No multi-file project support
- Cannot fully verify correctness without problem statement

## Future Improvements

Planned upgrades:

- Runtime execution engine
- Docker support
- Streaming responses
- Benchmark dashboard
- Monaco editor integration
- Multi-language support
- Automatic corrected-file saving
- Batch debugging workflows

## Engineering Concepts Demonstrated

This project demonstrates:

- Systems orchestration
- Backend engineering
- Compiler integration
- GPU acceleration
- Local AI deployment
- Prompt engineering
- Developer tooling
- Regex post-processing
- CUDA infrastructure setup
