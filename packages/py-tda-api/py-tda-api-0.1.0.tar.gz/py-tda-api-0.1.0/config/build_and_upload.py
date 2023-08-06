import shutil
import pathlib
import subprocess

JUST_BUILD = False

# Delete the Build Folder.
build_folder = pathlib.Path('build')
shutil.rmtree(path=build_folder, ignore_errors=True)

# Delet the Distribution Folder.
dist_folder = pathlib.Path('dist')
shutil.rmtree(path=dist_folder, ignore_errors=True)

# Grab the current working directory.
current_dir = pathlib.Path().cwd().as_posix()

# Run Build.
with subprocess.Popen('python setup.py sdist bdist_wheel', cwd=current_dir) as build_process:

    # Wait till we have the results.
    build_process.wait()

    # Only uploaded if needed.
    if JUST_BUILD is False:

        # Upload to TestPyPi.
        with subprocess.Popen('twine upload -r testpypi dist/*', cwd=current_dir) as twine_proc:
            twine_proc.wait()

        # Upload to PyPi.
        with subprocess.Popen('twine upload dist/*', cwd=current_dir) as twine_proc:
            twine_proc.wait()
