from distutils.core import setup

setup(
    name='ddb_local',
    version='0.1',
    packages=['ddb_local',],
    license='MIT',
    author="Woongbin Kang",
    author_email="pypi@wbk.one",
    url="https://github.com/wbkang/ddb_local",
    long_description="DynamoDBLocal Wrapper for Python",
    install_requires=["requests"],
)