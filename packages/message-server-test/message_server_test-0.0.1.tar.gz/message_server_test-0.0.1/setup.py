from setuptools import setup, find_packages

setup(name="message_server_test",
      version="0.0.1",
      description="message_server",
      author="gb_and_i",
      author_email="vaspupiy@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
