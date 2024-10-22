# Source: https://gabnotes.org/pip-tools-for-python-dependencies-management/

from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
REQUIREMENTS_DIR = BASE_DIR / "requirements"


@task
def update(ctx: Context, *, upgrade: bool = False, hashes: bool = False) -> None:
    common_args = "-q --allow-unsafe --resolver=backtracking --strip-extras"
    common_args += " --upgrade" if upgrade else ""
    common_args += " --generate-hashes" if hashes else ""

    with ctx.cd(REQUIREMENTS_DIR):
        ctx.run(
            f"pip-compile {common_args} 'requirements.in'",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} 'requirements-dev.in'",
            pty=True,
            echo=True,
        )


@task
def install(ctx: Context, dev: bool = False) -> None:
    # If requirements.txt is not present, create it
    if not (REQUIREMENTS_DIR / "requirements.txt").exists():
        update(ctx)

    command = "pip-sync requirements.txt"
    if dev:
        command += " requirements-dev.txt"

    with ctx.cd(REQUIREMENTS_DIR):
        ctx.run(command, pty=True, echo=True)
