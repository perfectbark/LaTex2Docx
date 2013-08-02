from distutils.core import setup
import py2exe

py2exe_options = dict(skip_archive=True,ascii=False)

setup(console=['Latex2docx.py'], options={'py2exe':py2exe_options},)