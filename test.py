from auto_gui import Progressing

# progressing.Progressing().pipeline("open_browser", "https://www.youtube.com/").pipeline("sleep", 5).pipeline("click", "academind").run()
Progressing().pipeline("click", "text", "create").pipeline("sleep", 1).pipeline("click", "image", "../../upload-icon.png").run()
