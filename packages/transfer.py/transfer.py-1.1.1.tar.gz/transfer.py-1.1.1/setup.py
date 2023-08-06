from distutils.core import setup, Extension
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
def main():
    setup(name="transfer.py",
          version="1.1.1",
          description="transfers a PyObject",
          long_description=README,
          url="https://github.com/jordan69420/transfer.py",
          author="<Jordan Alexander Sweetman>",
          author_email="jordan.a.sweetman@icloud.com",
          classifiers=[
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.7",
          ],
          ext_modules=[Extension("read_obj", ["read.c"]), Extension("write_obj", ["main.c"])])

if __name__ == "__main__":
    main()
