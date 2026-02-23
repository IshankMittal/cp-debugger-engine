# CP Debugger Engine

A fully offline, compiler-aware C++ debugging engine integrating native compilation analysis with CUDA-accelerated local LLM inference.
CP Debugger Engine is a hybrid compiler + AI system designed to debug competitive programming code entirely offline.Unlike typical LLM-based debugging tools, this system performs real g++ compilation checks first, then routes tasks intelligently to a locally hosted DeepSeek-Coder model running on a CUDA-accelerated llama.cpp backend.This creates a deterministic, structured debugging pipeline instead of naive prompt-based analysis.The entire system runs locally on Windows with no cloud dependencies.
