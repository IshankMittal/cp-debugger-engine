# CP Debugger Engine

**A fully offline, compiler-aware C++ debugging engine integrating native compilation analysis with CUDA-accelerated local LLM inference.**

## Overview
CP Debugger Engine is a hybrid systems project that combines traditional compilation with modern AI reasoning — fully offline.

Instead of blindly sending code to a language model, this system first performs a **real `g++` compilation check**, then intelligently routes the task to a locally hosted DeepSeek-Coder model running on a CUDA-accelerated `llama.cpp` backend.

Everything runs on your machine. No APIs. No cloud. No internet dependency.

This project demonstrates:

-Systems design

-Compiler integration

-Local LLM infrastructure



