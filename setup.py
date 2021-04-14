from setuptools import setup

setup(
   name='testbot321',
   version='1.0',
   description='A useful bot',
   author='MS',
   author_email='foomail@foo.com',
   packages=['tele_bot'],
   install_requires=['requests', 'telebot'], #external packages as dependencies
)