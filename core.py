"""核心业务逻辑函数，负责读取配置和模板信息。"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List

import yaml


def load_config(config_path: Path) -> Dict[str, object]:
    """读取配置文件并返回包含模型与参数信息的字典。

    参数:
        config_path: 配置文件的路径对象。

    返回:
        包含模型名称、温度、参数映射及输出文件路径的字典。
    """
    try:
        with config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    except FileNotFoundError as exc:
        print(f"读取配置文件失败，未找到文件: {exc}")
        raise
    except yaml.YAMLError as exc:
        print(f"解析配置文件失败，YAML 格式错误: {exc}")
        raise
    except Exception as exc:  # pylint: disable=broad-except
        print(f"读取配置文件时发生未知错误: {exc}")
        raise

    model_section = data.get("model", {}) if isinstance(data.get("model"), dict) else {}
    model_name = data.get("openai_model") or model_section.get("name")
    temperature = data.get("temperature")
    if temperature is None:
        temperature = model_section.get("temperature")

    params_data = data.get("params")
    if not isinstance(params_data, list):
        print("配置文件中的 params 字段缺失或格式不正确，应为包含字典的列表。")
        raise ValueError("params 字段格式错误")

    params: Dict[str, str] = {}
    for item in params_data:
        if not isinstance(item, dict):
            print("params 列表中的项目必须为字典，请检查配置文件。")
            raise ValueError("params 项格式错误")
        name = item.get("name")
        prompt = item.get("prompt")
        if not name or not prompt:
            print("params 项缺少 name 或 prompt 字段，请补充完整。")
            raise ValueError("params 信息缺失")
        params[name] = prompt

    output_file = data.get("output_file")
    if not output_file:
        output_section = data.get("output") if isinstance(data.get("output"), dict) else {}
        directory = output_section.get("directory")
        filename = output_section.get("filename")
        if directory and filename:
            output_file = str(Path(directory) / filename)

    return {
        "model_name": model_name,
        "temperature": temperature,
        "params": params,
        "output_file": output_file,
    }


def load_template(template_path: Path) -> Dict[str, object]:
    """读取模板文件并提取其中的占位符名称列表。

    参数:
        template_path: 模板文件的路径对象。

    返回:
        字典，包含模板内容与占位符名称列表。
    """
    try:
        template_text = template_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        print(f"读取模板文件失败，未找到文件: {exc}")
        raise
    except Exception as exc:  # pylint: disable=broad-except
        print(f"读取模板文件时发生未知错误: {exc}")
        raise

    placeholders: List[str] = []
    try:
        found = re.findall(r"{([^{}]+)}", template_text)
        seen = set()
        for name in found:
            if name not in seen:
                placeholders.append(name)
                seen.add(name)
    except re.error as exc:
        print(f"解析模板占位符失败，正则表达式错误: {exc}")
        raise

    return {"content": template_text, "placeholders": placeholders}


def validate_placeholders(template_placeholders: List[str], config_params: Dict[str, str]) -> None:
    """验证模板占位符是否与配置中的参数列表完全匹配。

    参数:
        template_placeholders: 模板中提取的占位符名称列表。
        config_params: 配置文件中的参数名称与提示语映射。

    返回:
        无返回值，如果存在不匹配情况则抛出异常。
    """
    template_set = set(template_placeholders)
    config_set = set(config_params.keys())

    missing_in_config = template_set - config_set
    missing_in_template = config_set - template_set

    if missing_in_config or missing_in_template:
        if missing_in_config:
            print(f"配置文件缺少以下占位符的提示语: {', '.join(sorted(missing_in_config))}")
        if missing_in_template:
            print(f"模板文件缺少以下配置的占位符: {', '.join(sorted(missing_in_template))}")
        raise ValueError("模板与配置占位符不一致")

__all__ = ["load_config", "load_template", "validate_placeholders"]
