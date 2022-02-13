# DataMiner
In this python project, we will mine a repository and conduct a few analyses. The project is divided into two parts.

## How to run data miner and perform fisher exact test
1. Create a virtual environment
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. Run the code
```
python main.py
```

<h2>Part 1</h2>
In this first part, we will iterate over the commits of a repository and collect git information about modifications.

There are several ways to mine software repositories. In this script, we will use the [PyDriller](https://pydriller.readthedocs.io/en/latest/index.html)
framework since it provides a simple way to extract information from any Git repository, such as commits, developers, 
modifications, diffs, and source codes. We will mine the commits from the main branch of the [JUnit4](https://github.com/junit-team/junit4/commits/main "Main branch") repository.

The goal is to answer the following questions:
- Who is the authors that modified more files?
- What is the commit hash that contain most modified lines?

<h2>Part 2</h2>
In the second part, we will run a smell detector tool in the initial commit of the system.

The goal is to learn how to run a third-party tool from terminal