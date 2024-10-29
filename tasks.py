from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)


@task
def build(ctx: Context, project: str, region: str, repo: str, name: str) -> None:
    with ctx.cd(BASE_DIR):
        image_name = f"{region}-docker.pkg.dev/{project}/{repo}/{name}"
        ctx.run(
            f"docker compose -f docker-compose.production.yml build",
            pty=True,
            echo=True,
        )


@task
def deploy(ctx: Context, project: str, region: str, repo: str, name: str) -> None:
    with ctx.cd(BASE_DIR):
        image_name = f"{region}-docker.pkg.dev/{project}/{repo}/{name}"
        ctx.run(
            f"docker push {image_name}",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"gcloud run deploy {name} --region {region} --image {image_name}",
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
