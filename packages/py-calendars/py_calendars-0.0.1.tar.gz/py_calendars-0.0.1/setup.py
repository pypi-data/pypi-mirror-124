import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_calendars",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Suraj S", 
    author_email="www.surajsuraj7600@gmail.com",                   
    description="To print the calendar design on the terminal ",
    long_description=long_description,   
    long_description_content_type="text/markdown",
    url= "https://github.com/surajs123/pycalendar",
    packages=setuptools.find_packages(where="src"),   
    project_url={
        "Bug Tracker":"https://github.com/surajs123/pycalendar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',               
    package_dir={"":"src"},           
   
   
)