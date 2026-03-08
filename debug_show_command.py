import os
from CLIByAI.llm_client import generate_command

def main():
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'prompt3.md')
    prompt = ''
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()

    res = generate_command('What is my IP address?', prompt)
    # Print only the command (user requested minimal output)
    print(res.get('command', ''))


if __name__ == '__main__':
    main()
