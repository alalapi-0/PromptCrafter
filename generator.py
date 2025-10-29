"""与 OpenAI 模型交互的生成模块。"""
from __future__ import annotations

import os
from typing import Dict, List

import openai


def _prepare_api_key() -> None:
    """从环境变量读取 API Key 并配置 OpenAI SDK。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("未找到 OPENAI_API_KEY 环境变量，无法调用 OpenAI 接口。")
    openai.api_key = api_key


def _extract_choices(response: object) -> List[Dict[str, object]]:
    """从 OpenAI 响应对象中提取 choices 列表。"""
    if hasattr(response, "choices"):
        choices = getattr(response, "choices")
        if isinstance(choices, list):
            return choices
    if isinstance(response, dict):
        choices = response.get("choices")
        if isinstance(choices, list):
            return choices
    try:
        choices = response["choices"]  # type: ignore[index]
        if isinstance(choices, list):
            return choices
    except Exception:  # pylint: disable=broad-except
        pass
    return []


def generate_param(prompt_text: str, model: str, temperature: float) -> str:
    """调用 OpenAI ChatCompletion 接口，根据提示语生成单个参数内容。

    参数:
        prompt_text: 要发送给模型的提示语内容。
        model: 使用的模型名称，例如 "gpt-4"。
        temperature: 控制随机性的温度参数。

    返回:
        模型返回的文本内容字符串。
    """
    _prepare_api_key()

    if not prompt_text:
        raise ValueError("提示语不能为空")

    request_params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt_text}],
    }
    if temperature is not None:
        request_params["temperature"] = temperature

    try:
        response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            **request_params,
        )
    except Exception as exc:  # pylint: disable=broad-except
        raise RuntimeError(f"调用 OpenAI 接口失败: {exc}") from exc

    choices = _extract_choices(response)
    if not choices:
        raise RuntimeError("OpenAI 接口未返回任何结果")

    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not message or not isinstance(message, dict) or "content" not in message:
        raise RuntimeError("OpenAI 接口返回的数据格式不符合预期")

    return str(message["content"]).strip()


def generate_all(params: List[Dict[str, str]], model: str, temperature: float) -> Dict[str, str]:
    """遍历配置中的参数提示语，依次调用模型生成所有字段内容。

    参数:
        params: 参数配置列表，每项包含 name 与 prompt 字段。
        model: 使用的模型名称，例如 "gpt-4"。
        temperature: 控制随机性的温度参数。

    返回:
        由参数名称映射到生成内容的字典。
    """
    results: Dict[str, str] = {}
    for item in params:
        name = item.get("name")
        prompt = item.get("prompt")
        if not name or not prompt:
            raise ValueError("参数配置缺少 name 或 prompt 字段")

        print(f"🎯 正在生成：{name} ...", end=" ")
        generated = generate_param(prompt, model, temperature)
        results[name] = generated
        print(f"完成：{generated}")

    return results


__all__ = ["generate_param", "generate_all"]
