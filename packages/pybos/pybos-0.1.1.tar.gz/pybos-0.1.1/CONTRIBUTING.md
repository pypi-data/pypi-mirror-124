# Contributing

First off, thank you for considering contributing to pyBOS.
It's people like you that make pyBOS such a great tool.

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Following these guidelines helps to communicate that you respect
the time of the developers managing and developing this project.
In return, they should reciprocate that respect in addressing your issue, assessing changes,
and helping you finalize your pull requests.

For any questions not concerning directly pyBOS, 
read the docs, ask Google, look on Stack Overflow (in this order).

If your problem is indeed pyBOS specific,
ask one of the maintainers by writing an [issue on GitLab](https://gitlab.coria-cfd.fr/pouxa/pybos/issues).

The current stable version is in the branch `master`  
The branch `next` contains beta developments that will regularly be merged with `master` for each new version.   
All other future developments are on their respective branches and will be merged into `next`

## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs directly our [issues list on GitLab](https://gitlab.coria-cfd.fr/pouxa/pybos/issues).

Please include,
 * the version of pyBOS
    ```python 
    import pybos  
    print(pybos.version)
    ``` 
 * detailed steps to reproduce the bug.

If you don't have steps to reproduce the bug,
just note your observations in as much detail as you can.

### Suggest features or enhancement

If you find yourself wishing for a feature that doesn't exist in pyBOS,
you are probably not alone. There are bound to be others out there with similar needs.

Any code or part of a script that you expect to be used multiple times
is relevelant for being included in this library.  

Open an issue on our [issues list on GitLab](https://gitlab.coria-cfd.fr/pouxa/pybos/issues): 

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

### Fix bugs

Look through the [GitLab issues](https://gitlab.coria-cfd.fr/pouxa/pybos/issues) for bugs.

### Implement features or enhancement

Look through the [GitLab issues](https://gitlab.coria-cfd.fr/pouxa/pybos/issues) for missing features.
Please do not combine multiple feature enhancements into a single pull request.

## Setting Up the Code for Local Development

1. Clone the project locally.  
   ```shell
   git clone git@gitlab.coria-cfd.fr:pouxa/pybos.git
   ```

2. Install your local copy into a virtualenv.  
   ```shell
   cd pybos  
   python3 -m pybos-venv  
   source pybos-venv/bin/activate  
   pip install -e .
   ```

3. Create a branch for local development.  
   ```shell
   git checkout -b name-of-your-bugfix-or-feature
   ```
    
4. Make a lot's of little commits while you work
   ```shell
   git add ...  
   git commit -m "Your detailed description of your changes"  
   git push origin name-of-your-bugfix-or-feature
   ```  

5. Document your work using docstrings

6. When you are fully satisfied
 - merge the current state of the `next` branch  
   ```shell
   git merge next
   ```  
 - make a [push request](https://gitlab.coria-cfd.fr/pouxa/pybos/branches)  
   which will alert the main contributers and they will finish to merge your developments.

## Contributor Guidelines

### Coding Standards

* English language 
* PEP8
    - documentation 
        - [official documentation](https://www.python.org/dev/peps/pep-0008/)
        - [synthesis from realpython](https://realpython.com/python-pep8/)
        - [french synthesis from openclassroom](https://tinyurl.com/y6q2wfqq)
    - use tools for checking it
        - [pycodestyle](https://pypi.org/project/pycodestyle/)
        - [flake8](https://pypi.org/project/flake8/)
        - [pylint](https://pypi.org/project/pylint/)
    - Specifically : 
        - explicit variable names
        - no tabulation but 4 spaces
        - maximum line length of 120 
* type hinting with [Mypy](https://mypy.readthedocs.io/en/latest/)   
  specify types of arguments and returns of functions

## Core Committer Guide

- limit the number of dependencies
- minimize duplication
- maximize the versatility (your function should be usable in a variety of context)