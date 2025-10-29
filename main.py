"""PromptCrafter 主程序入口，负责初始化读取流程。"""
from __future__ import annotations

from pathlib import Path

from core import load_config, load_template, validate_placeholders


def main() -> None:
    """启动程序，读取配置与模板并输出待生成的提示语信息。"""
    project_root = Path(__file__).resolve().parent
    config_path = project_root / "config.yaml"
    template_path = project_root / "prompts" / "template.txt"

    try:
        template_info = load_template(template_path)
        placeholders = template_info["placeholders"]
        print("🧩 模板读取成功，占位符如下：")
        for name in placeholders:
            print(f"  - {name}")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"读取模板时发生错误，程序终止: {exc}")
        return

    try:
        config = load_config(config_path)
        validate_placeholders(placeholders, config["params"])
    except Exception as exc:  # pylint: disable=broad-except
        print(f"读取配置或校验占位符时发生错误，程序终止: {exc}")
        return

    model_name = config.get("model_name") or "未指定模型"
    temperature = config.get("temperature")
    temperature_text = f"，温度 {temperature}" if temperature is not None else ""
    print(f"\n📖 配置文件读取成功，将调用模型 {model_name}{temperature_text}")
    for name, prompt in config["params"].items():
        print(f"  - {name}: {prompt}")

    output_file = config.get("output_file")
    if output_file:
        print(f"\n📝 生成结果将保存至: {output_file}")

    print("\n✅ 准备完毕，可进入下一步：调用模型生成参数值")


if __name__ == "__main__":
    main()
