Developer Documentation
#######################

This document provides information for developers who want to contribute to the development of ``ucc``, as well as for maintainers.

Creating a release
==================

.. important::
    This section is intended for maintainers of the :code:`ucc` repository.

To release a new version of ``ucc`` on GitHub, follow the steps below.

1. **Bump the Version:**
    - Increment the version in ``pyproject.toml`` according to `semantic versioning <https://semver.org/>`_.

2. **Update the Changelog:**
    - Update the ``CHANGELOG.rst`` file with all new changes, improvements, and bug fixes since the previous release.

3. **Commit Changes:**
    - Commit the changes to ``pyproject.toml`` and `CHANGELOG.rst` and open a PR to get the changes reviewed.

4. **Create a New Tag:**
    - Once the PR is merged, pull the changes to your local repository.
    - Create a new Git tag for the release. The tag name should match the version number (e.g., ``v1.1.0``).

    .. code-block:: bash

        git tag v1.1.0
        git push origin v1.1.0

5. **Draft a New Release on GitHub:**
    - Navigate to https://github.com/unitaryfoundation/ucc/releases to create a new release.
    - Select the newly created tag.
    - Fill in the release title and description, and copy the changelog entry for the description.
    - Publish the release.

.. tip::
    Ensure that all changes pass the tests, and the documentation builds correctly before creating a release.


Publishing a new version of UCC to PyPI (maintainers only)
==========================================================
1. Follow the steps above for creating a new release.
2. The deployment to TestPyPI should trigger automatically (only maintainers will have access).
3. Run a test of the TestPyPI deployment on your local machine:
    a. Create a new python environment > our latest required version, e.g. `python3.13 -m venv ~/.venvs/test_ucc`
    b. Run `pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ucc` to install from the TestPiPY deployment
    c. Run `python -c "import ucc; print(ucc.__version__)"`. This should run successfully and (theoretically) show the latest version of UCC (bug [#312](#312).
4. If all went well in the TestPyPI step, you (as a maintainer) can go to the GH Actions and approve the deployment to real PyPI.
    If for some reason this does not work, or fails to trigger on a release, you can also manually trigger the workflow in the Github Actions tab:
    <img alt="Image" width="614" src="https://private-user-images.githubusercontent.com/15827191/424737759-ba17ac1b-26f1-402a-b050-f75b72b8ee14.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDM0NTYwNjksIm5iZiI6MTc0MzQ1NTc2OSwicGF0aCI6Ii8xNTgyNzE5MS80MjQ3Mzc3NTktYmExN2FjMWItMjZmMS00MDJhLWIwNTAtZjc1YjcyYjhlZTE0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAzMzElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMzMxVDIxMTYwOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTQ5NmM2OWI4ZjdkMDkwNjIyYzM4MGY0MzU0MDRlMjY5ZDJlZTY5MWNjZTExZTgxYjNmOWNmZmMwZWQ0NmM0MWMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.3KNkSh1wDwsDLndkVyjcJhcwXe9ujEt67QSSMcMoyOc"> <img alt="Image" width="328" src="https://private-user-images.githubusercontent.com/15827191/424737760-ec8ad61a-58b0-403e-bbd7-9eefd18a7150.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDM0NTYwNjksIm5iZiI6MTc0MzQ1NTc2OSwicGF0aCI6Ii8xNTgyNzE5MS80MjQ3Mzc3NjAtZWM4YWQ2MWEtNThiMC00MDNlLWJiZDctOWVlZmQxOGE3MTUwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAzMzElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMzMxVDIxMTYwOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTkwNzVmYTFmMGRkZTYxNGRiYjk3MDk0YmM2YmY4YzQyZGU4NjZkYjQ4ZmRjMmZjNzFhYTc5OTYzOGExZTI4MDcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.08y9yC6cMZO76ulR9by2CNtk1qxDPwWIoptzeZAzh5E"> <img alt="Image" width="402" src="https://private-user-images.githubusercontent.com/15827191/424737761-c1392774-68a1-4f37-a34a-e3b411d8e451.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDM0NTYwNjksIm5iZiI6MTc0MzQ1NTc2OSwicGF0aCI6Ii8xNTgyNzE5MS80MjQ3Mzc3NjEtYzEzOTI3NzQtNjhhMS00ZjM3LWEzNGEtZTNiNDExZDhlNDUxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAzMzElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMzMxVDIxMTYwOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWNhNjc3NmIxNTJmNzdiMGMzM2MwZDRjNTgyNTM3MDNiOTVjMjk1NjY1N2UwZWQwMzY2ODZkNGNkMmVkOWQ2NmQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.wHrcgKjrYMmITJa1FcZJEI5yug8enJbjduHekAA6qi4">
