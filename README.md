### Installing and running the python server:
1. run `pip3 install -r requirements.txt` (you might use pip instead of pip3)
2. run `python3 -m main` to start the processing server (you might use python instead of python3)

### Installing and running the extension or bookmarklet:
- See the readme at [wikitrust_ui/extension/README.md](./wikitrust_ui/extension/README.md)

### Wikitrust File Structure
- `docs`: Contains all documentation related to the project.
- `wikitrust`: Contains all Python packages related to computation and storage.
    - `computation_engine`: Contains all Python source related to calculation of trust and reputation.
    - `database_engine`: Contains schema and controller for Wikitrust database.
    - `storage_engine`: Contains Python source related to storage of Wikipedia text.
    - `test`: Contains tests that test the `wikitrust` package.
- `wikitrust_ui`: Contains all source code related to visualization of Wikitrust data.
-`README.md`: Readme containing project overview
- `test.py`: Python script running all tests for project

### Style Best Practices
- All files should have a header describing contents of file.
- All functions should have docstring describing it. (Following Epydoc structure http://epydoc.sourceforge.net/)
```
"""
Comment describing function.
@param param1: this is a first param
@param param2: this is a second param
@return: this is a description of what is returned
@raise keyError: raises an exception
"""
```
- All code should have type annotations to the extent possible.
- Limit inline comments unless necessary. (Do not add comments to self descriptive code)


### Branching Guidelines
There are only two branches that will always be present, **master** and **develop**. For  **develop** to be merged into **master**,  a pull request must be created and all code must have been reviewed by the whole team and Luca de Alfaro.  All feature branches should branch off and back into **develop**. For a feature branch to merge into **develop**, a pull request must be created and all code must be reviewed by at least two other individuals who are not working on that feature. Optionally but reccomended, when merging from any sub branches onto a feature branch, the whole team working on that feature branch should review the code being merged. In general, for any merge apart from a merge into **master**, create a pull request, add your reviewers to the pull request on GitHub and add Eric Vin as assignee.  For any merge apart from a into **master**, create a pull request, add Luca de Alfaro as reviewer and assignee. Once a branch has been merged back into another branch and no further work will be done on it. delete that branch from GitHub.

#### Branching Checklist
- Create a pull request with your changes.
- Assign your reviewers to the pull request (Luca for **Master**, two individuals on another project for **develop**, etc...).
- Assign your assignee (Eric for **develop**, Luca for **Master**)
- Before any merge to **master** update `README.md` with current version.
- Before any merge to **master**, `docs` folder should be updated with most recent documentation from Google Drive.
- After merging to **master**, tag the commit in git with the version number for ease of reference and deployment.
