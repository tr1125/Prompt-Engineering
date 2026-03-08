from CLIByAI.gradio_app import build_ui


def main():
    app = build_ui()
    app.launch()


if __name__ == "__main__":
    main()
