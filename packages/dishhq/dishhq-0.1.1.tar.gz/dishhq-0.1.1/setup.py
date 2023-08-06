
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dishhq",                     
    version="0.1.1",                        
    author="Dish Team",                    
    description="Official Python SDK for Dish",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),   
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                    
    python_requires='>=3.6',           
    py_modules=["dishhq"],        
    package_dir={'':'.'},     
    install_requires=[]                     
)