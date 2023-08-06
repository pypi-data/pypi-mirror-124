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

# Grab the test files.
test_folder = pathlib.Path('tests')
test_folder_td = pathlib.Path('td/tests/')
shutil.copytree(
    src=test_folder,
    dst=test_folder_td,
    symlinks=False,
    dirs_exist_ok=True
)

# Grab the sample files.
sample_folder = pathlib.Path('samples')
sample_folder_td = pathlib.Path('td/samples/')
shutil.copytree(
    src=sample_folder,
    dst=sample_folder_td,
    symlinks=False,
    dirs_exist_ok=True
)

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

# Remove the sample and test folder.
shutil.rmtree(path=test_folder_td, ignore_errors=True)
shutil.rmtree(path=sample_folder_td, ignore_errors=True)
