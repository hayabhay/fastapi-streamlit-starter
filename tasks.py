# Source: https://gabnotes.org/pip-tools-for-python-dependencies-management/

from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
REQUIREMENTS_DIR = BASE_DIR / "requirements"


@task
def update(ctx: Context, *, upgrade: bool = False) -> None:
    common_args = (
        "-q --allow-unsafe --resolver=backtracking --strip-extras --generate-hashes"
    )
    if upgrade:
        common_args += " --upgrade"

    with ctx.cd(REQUIREMENTS_DIR):
        # Create requirements.txt and requirements-dev.txt
        MAIN_REQ = BASE_DIR / "requirements.txt"
        DEV_REQ = BASE_DIR / "requirements-dev.txt"

        ctx.run(
            f"pip-compile {common_args} 'main.in' -o {MAIN_REQ}",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} 'dev.in' -c {MAIN_REQ} -o {DEV_REQ}",
            pty=True,
            echo=True,
        )


@task
def install(ctx: Context, dev: bool = False) -> None:
    # If requirements.txt is not present, create it
    if not (BASE_DIR / "requirements.txt").exists():
        update(ctx)

    command = "pip-sync requirements.txt"
    if dev:
        command += " requirements-dev.txt"

    with ctx.cd(BASE_DIR):
        ctx.run(command, pty=True, echo=True)
