# flake8: noqa
import os
import tempfile

import nox


nox.options.sessions = "lint", "mypy"

locations = "make_pycco_pages.py", "src"


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.10"])
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "mypy",
    )
    session.run("mypy", *args)


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)

    os.unlink(requirements.name)
