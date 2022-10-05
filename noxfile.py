import os
import tempfile

import nox


locations = "noxfile.py", "make_pycco_pages.py", "day1", "day2"


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8")
    session.run("flake8", *args)


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
