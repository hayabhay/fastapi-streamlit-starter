from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
REQUIREMENTS_DIR = BASE_DIR / "requirements"


@task
def update(ctx: Context, upgrade: bool = False, hashes: bool = False) -> None:
    args = "-q --allow-unsafe --resolver=backtracking --strip-extras"
    args += " --upgrade" if upgrade else ""
    args += " --generate-hashes" if hashes else ""

    with ctx.cd(REQUIREMENTS_DIR):
        ctx.run(
            f"pip-compile {args} 'requirements.in'",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {args} 'requirements-dev.in'",
            pty=True,
            echo=True,
        )


@task
def install(ctx: Context, dev: bool = False) -> None:
    # If requirements.txt is not present, create it
    if not (REQUIREMENTS_DIR / "requirements.txt").exists():
        update(ctx)

    command = "pip-sync requirements.txt"
    command += " requirements-dev.txt" if dev else ""

    with ctx.cd(REQUIREMENTS_DIR):
        ctx.run(command, pty=True, echo=True)


@task
def build(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        image_name = "us-west1-docker.pkg.dev/<project_id>/<repo>/<fapi-starter>"
        ctx.run(
            f"docker build --target api --tag {image_name} .",
            pty=True,
            echo=True,
        )


@task
def deploy(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        image_name = "us-west1-docker.pkg.dev/<project_id>/<repo>/<fapi-starter>"
        ctx.run(
            f"docker push {image_name}",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"gcloud run deploy <fapi-starter> --region us-west1 --image {image_name}",
            pty=True,
            echo=True,
        )


@task
def gitprep(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("git add .", pty=True, echo=True)
        ctx.run("pre-commit run", pty=True, echo=True)


@task
def gitpush(ctx: Context, message: str) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run(f'git commit -am "{message}"', pty=True, echo=True)
        ctx.run("git push ", pty=True, echo=True)