from hi.utils.exec import run_stream_command

def build(path = "."):
    run_stream_command(f"cd {path}; npm run build")

def install(path = "."):
    run_stream_command(f"cd {path}; npm install")

def publish(path = "."):
    run_stream_command(f"cd {path}; npm publish")
