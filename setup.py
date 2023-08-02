import setuptools
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = "NoneBot lostark cn wandering trader plugin"

setuptools.setup(
    name="nonebot_plugin_lostark_wandering_trader",
    version="0.0.2",
    author="EmiyaGm",
    author_email="464723943@qq.com",
    description="NoneBot lostark cn wandering trader plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmiyaGm/nonebot-plugin-lostark-wandering-trader",
    project_urls={
        "Bug Tracker": "https://github.com/EmiyaGm/nonebot-plugin-lostark-wandering-trader/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["nonebot_plugin_lostark_wandering_trader"],
    python_requires=">=3.8,<4.0",
    install_requires=[
        "nonebot2>=2.0.0",
        "httpx>=0.20.0,<1.0.0",
        "nonebot-adapter-onebot>=2.0.0",
        "nonebot-plugin-apscheduler>=0.3.0",
        "nonebot2[fastapi]>=2.0.0",
    ],
)