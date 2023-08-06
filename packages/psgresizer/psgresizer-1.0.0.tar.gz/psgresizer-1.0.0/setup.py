import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="psgresizer",
    version="1.0.0",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="Resize images, write to disk and encode them to Base64 all at once in this PySimpleGUI Demo Program.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Image_Resize_and_Base64_Encode.pyw",
    packages=['psgresizer'],
    install_requires=['PySimpleGUI', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ],
    package_data={"":["*.ico"]},
    entry_points={
        'gui_scripts': [
            'psgresizer=psgresizer.gui:main'
        ],
    },
)
