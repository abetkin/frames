

def log_ast_tree():
    1

def log_events():
    names = await Event.loadNames
    for name in names:
        await log_name(name)

def log_name(name):
    nam = await Test.name
    if nam == name:
        print(time)