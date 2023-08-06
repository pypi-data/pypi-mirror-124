from shutil import ExecError
import subprocess

def run_stream_command(command):
    if ";" in command:
        commands = ["bash", "-c", command]
    else:
        commands = command.split(" ")

    process = subprocess.Popen(commands)
    process.communicate()[0]

    p_status = process.wait()
    if process.returncode:
        raise ExecError(f":: Command execution returned { process.returncode }: " + process.stdout.decode().strip())


def run_command(command):
    process = subprocess.run(command, capture_output=True, shell=True)
    if process.returncode:
        raise ExecError(f":: Command execution returned { process.returncode }: " + process.stderr.decode().strip())

    return process.stdout.decode().strip()
