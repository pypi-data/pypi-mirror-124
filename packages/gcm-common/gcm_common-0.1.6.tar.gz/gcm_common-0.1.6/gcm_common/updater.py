import compileall
import os
import shutil
from datetime import datetime
from pathlib import Path
from shutil import copyfile


def update():
    for subdir, dirs, files in os.walk("."):
        if 'venv' in subdir or '.env' in subdir:
            continue
        if '__pycache__' in subdir:
            shutil.rmtree(subdir)

    compileall.compile_dir('.')
    if os.path.exists('update'):
        shutil.rmtree('update')

    Path('update').mkdir(parents=True, exist_ok=True)

    for subdir, dirs, files in os.walk("."):
        if 'git' in subdir or 'update' in subdir or '.idea' in subdir or subdir.startswith(
                '.\\log') or 'venv' in subdir or 'test' in subdir:
            continue

        if '__pycache__' in subdir:
            for file in files:
                if 'update' in file:
                    continue
                filename = os.path.join('update', subdir.replace('__pycache__', '')) + file
                filename = filename.replace('.cpython-36', '')
                copyfile(os.path.join(subdir, file), filename)
            continue

        Path(os.path.join('update'), subdir).mkdir(parents=True, exist_ok=True)

        for file in files:
            if 'git' in file or file.endswith('.py') or file.endswith('.zip') or file.endswith('.md') or file.endswith(
                    '.jpg'):
                continue
            filename = os.path.join('update', subdir) + '\\' + file
            copyfile(os.path.join(subdir, file), filename)

    now = datetime.now()
    output_filename = 'update' + now.strftime('%Y%m%d-%H%M')
    shutil.make_archive(output_filename, 'zip', "update")
