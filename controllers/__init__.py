import os


cwd = os.path.abspath(
    os.path.join(
        os.path.dirname( __file__ ),
        '..',
        'application'))

os.chdir(cwd)

print(os.getcwd())