from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(name='distributions-udacity-akshayudayahegde',
      version='0.1.0',
      description='Gaussian and Binomial Distribution Basic Functions',
      packages=['distributions'],
      author="Akshay Udaya Hegde",
      author_email="akshayudayhegde2@gmail.com",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
