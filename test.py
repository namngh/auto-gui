from auto_gui import progressing

# progressing.Progressing().pipeline("open_browser", "https://www.youtube.com/").pipeline("sleep", 5).pipeline("click", "academind").run()
progressing.Progressing().pipeline("click", "create").pipeline("sleep", 1).pipeline("click", "upload").run()
