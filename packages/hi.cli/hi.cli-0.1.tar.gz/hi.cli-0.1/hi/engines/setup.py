import requests
import shutil
import os
from sys import platform

from hi.utils.exec import run_stream_command, run_command


def helm():
    print(":: Installing Helm")
    if platform == "darwin":
        run_stream_command("brew install helm")
    else:
        path = "/tmp/get-helm-3.sh"
        resp = requests.get("https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3")
        with open(path, "w") as f:
            f.write(resp.content.decode())

        os.chmod(path, 0o755)
        run_stream_command("bash /tmp/get-helm-3.sh")
        os.remove(path)


    print(":: Installing Helm s3 plugin")
    run_stream_command("helm plugin install https://github.com/hypnoglow/helm-s3.git")
    
    print(":: Adding our repo")
    try:
        run_stream_command("helm repo add hi-charts s3://hi-charts")
        run_stream_command("helm repo update")
    except:
        print("Couldn't add our repo.")

# def helmfile():
#     resp = requests.get("https://api.github.com/repos/roboll/helmfile/releases/latest")
#     assets = json.loads(resp.content)['assets']
#     for a in assets:
#         if a["name"] == f"helmfile_{ platform }_amd64":
#             download_url = a['browser_download_url']

#     with requests.get(download_url, stream=True) as r:
#         with open("/tmp/helmfile", 'wb') as f:
#             shutil.copyfileobj(r.raw, f)

#     shutil.move("/tmp/helmfile", "/usr/local/bin/helmfile")
#     os.chmod('/usr/local/bin/helmfile', 0o755)

def kubectl():
    print(":: Installing kubectl")
    if platform == "darwin":
        run_stream_command("brew install kubectl")
    elif platform == "linux" or platform == "linux2":
        resp = requests.get('https://dl.k8s.io/release/stable.txt')
        version = resp.content.decode().strip()

        download_file(f"https://dl.k8s.io/release/{ version }/bin/linux/amd64/kubectl", "/tmp/kubectl")

    shutil.move("/tmp/kubectl", "/usr/local/bin/kubectl")
    os.chmod('/usr/local/bin/kubectl', 0o755)

def aws_google_auth():
    print(":: Installing aws-google-auth")
    if platform == "darwin":
        run_stream_command("brew install aws-google-auth")


def download_file(url, dest):
        with requests.get(url, stream=True) as r:
            with open(dest, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
