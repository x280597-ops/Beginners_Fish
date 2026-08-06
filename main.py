import read_files
gamelist=read_files.load_file()
for game in gamelist:
    game()

    