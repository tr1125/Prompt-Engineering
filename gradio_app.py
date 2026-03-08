import os
import gradio as gr

from CLIByAI.llm_client import generate_command


def translate_handler(instruction: str):
    prompt_text = ""
    try:
        p = os.path.join(os.path.dirname(__file__), "prompts", "prompt3.md")
        with open(p, "r", encoding="utf-8") as f:
            prompt_text = f.read()
    except Exception:
        prompt_text = ""

    result = generate_command(instruction, prompt_text)
    command = result.get("command", "")
    if not command:
        return result.get("explanation", "(no response)")
    return command


def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# CLIByAI — Generated command")
        instr = gr.Textbox(lines=3, label="Instruction")
        translate_btn = gr.Button("Translate")
        output_cmd = gr.Textbox(lines=10, label="Generated command")

        translate_btn.click(fn=translate_handler, inputs=[instr], outputs=[output_cmd])

    return demo


if __name__ == "__main__":
    build_ui().launch()
