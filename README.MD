# Ollama Intern
Very inspired by [open-interpreter](https://github.com/KillianLucas/open-interpreter), this is an attempt to learn & have a simple custom implementation for my local machine.

Imagine working with an IT intern, you test them, asking them questions, and they might answer right or wrong. If they answer mostly wrong, ~~fire them~~ send them to A100 and retrain/finetune them (not supported in this repo 😅). If they answer mostly right, you can get some help on simple works. Nice.

A work in progress and still very crude but should be easily understood. 

It communicates directly with [Ollama](https://github.com/jmorganca/ollama/).

Some quick notes on my setup:
- `conda` & `poetry` for managing environment and packages
- Windows Docker Desktop
- Setup Ollama with Docker following its [guide](https://hub.docker.com/r/ollama/ollama)
- I use [DeepSeek Coder 6.7B Instruct - GGUF by TheBloke](https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF) (You can use other GGUF model.)
- Use `requests` and `json` in Python to communicate with Ollama API at `localhost:11434` (default port)
- I use some prompts to force the local LLM only generate code (not always succeed, need more trial & error, or a bigger model). I also use a custom template, a little bit different from the Modelfile template provided by [Ollama Modelfile Library for DeepSeek Coder](https://ollama.ai/library/deepseek-coder/tags)
- Ask user if they want to execute the code
- Execute the (shell/command prompt) commands with `subprocess`

## Can I run a local LLM?
For GGUF models, it depends mostly on your available RAM. TheBloke GGUF model pages have tables that show the estimates of RAM needed for certain model and quantizations.

If you have a newer model of Nvidia GPU, you can safely assume that the weights can be offloaded to GPU VRAM. Read [Ollama's Docker page](https://hub.docker.com/r/ollama/ollama) carefully on how to utilize GPU in the container.

Personally, I have:
- RTX 3060 ~6GB VRAM
- ~16GB RAM

and I can run the 7B models in any quantization. For the 13B models, I haven't succeed in tweaking the settings to generate a token faster than 1 token/sec.

## Disclaimer
Please be careful, LLM may generate dangerous commands in your device. The LLM trainer and I am not responsible for that, use at your own risks.