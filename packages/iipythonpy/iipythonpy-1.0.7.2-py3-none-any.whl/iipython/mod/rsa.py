# Copyright 2021 iiPython

# Modules
import shutil
import subprocess

# Fast keygen function
def fast_keygen(bits: int = 4096) -> tuple:
    if not shutil.which("openssl"):
        class OpenSSLNotInstalled(Exception):
            pass

        raise OpenSSLNotInstalled

    s = subprocess.run(
        ["openssl", "genrsa", str(bits)],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    return (
        s.stdout.decode("utf8").split("-----")[2].strip("\n"),
        int(s.stderr.decode("utf8").split(" (0x")[0].split("is ")[1])
    )
