from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = 'An automation script to automate the process of creating a new GitHub repository, cloning it to the right directory and sub-directory and finally starting writing code'
  
setup(
        name ='projectauto',
        version ='1.0.1',
        author ='shy-tan',
        author_email ='iabdullahbintahir@gmail.com',
        url ='https://github.com/shy-tan/project-automation',
        description ='Automate the new-GitHub-project-creation process!',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'project = project.script:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='automation script  python package',
        install_requires = requirements,
        zip_safe = False
)