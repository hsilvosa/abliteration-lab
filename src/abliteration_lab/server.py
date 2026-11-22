"""Start and stop a llama-server process for one GGUF model."""

from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import requests

from .config import ModelSpec
from .paths import RESULTS_DIR


class LlamaServer:
    """Context manager around `llama-server` bound to localhost.

    The server exposes the OpenAI-compatible /v1/chat/completions endpoint plus
    llama.cpp `timings` in each response, used for tokens/second.
    """

    def __init__(self, spec: ModelSpec, server_cfg: dict[str, Any], overrides: dict[str, Any] | None = None):
        self.spec = spec
        self.cfg = {**server_cfg, **(overrides or {})}
        self.proc: subprocess.Popen | None = None
        self.log_path = RESULTS_DIR / "logs" / f"{spec.id}.server.log"

    @property
    def base_url(self) -> str:
        return f"http://{self.cfg['host']}:{self.cfg['port']}"

    def command(self) -> list[str]:
        binary = self.cfg.get("binary") or shutil.which("llama-server")
        if not binary:
            raise FileNotFoundError("llama-server not found on PATH; set [server].binary in configs/eval.toml")
        model_path: Path = self.spec.main_file
        if not model_path.exists():
            raise FileNotFoundError(f"{model_path} missing. Run: abl download --model {self.spec.id} --yes")
        cmd = [
            binary,
            "-m", str(model_path),
            "--host", str(self.cfg["host"]),
            "--port", str(self.cfg["port"]),
            "-c", str(self.cfg["ctx_size"]),
            "-ngl", str(self.cfg["gpu_layers"]),
            "-t", str(self.cfg["threads"]),
            "-fa", str(self.cfg["flash_attn"]),
            "--jinja",
            "--reasoning-format", "deepseek",   # reasoning goes to `reasoning_content`
            "--no-webui",
            "-np", "1",
        ]
        if self.cfg.get("n_cpu_moe"):
            cmd += ["--n-cpu-moe", str(self.cfg["n_cpu_moe"])]
        return cmd

    def __enter__(self) -> "LlamaServer":
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        log = self.log_path.open("w", encoding="utf-8")
        self.proc = subprocess.Popen(self.command(), stdout=log, stderr=subprocess.STDOUT)
        self._wait_healthy(float(self.cfg.get("startup_timeout_s", 300)))
        return self

    def _wait_healthy(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.proc and self.proc.poll() is not None:
                raise RuntimeError(f"llama-server exited early; see {self.log_path}")
            try:
                if requests.get(f"{self.base_url}/health", timeout=2).status_code == 200:
                    return
            except requests.RequestException:
                pass
            time.sleep(2)
        self.__exit__(None, None, None)
        raise TimeoutError(f"llama-server not healthy after {timeout:.0f}s; see {self.log_path}")

    def __exit__(self, *exc) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None

    def chat(self, prompt: str, *, temperature: float, max_tokens: int, seed: int, thinking: str) -> dict[str, Any]:
        body: dict[str, Any] = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "seed": seed,
        }
        if thinking == "off":
            body["chat_template_kwargs"] = {"enable_thinking": False}
        r = requests.post(f"{self.base_url}/v1/chat/completions", json=body, timeout=600)
        r.raise_for_status()
        data = r.json()
        msg = data["choices"][0]["message"]
        timings = data.get("timings", {})
        return {
            "content": msg.get("content") or "",
            "reasoning": msg.get("reasoning_content") or "",
            "finish_reason": data["choices"][0].get("finish_reason"),
            "completion_tokens": data.get("usage", {}).get("completion_tokens"),
            "tok_per_s": timings.get("predicted_per_second"),
            "prompt_tok_per_s": timings.get("prompt_per_second"),
        }
