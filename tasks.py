from invoke import task


@task
def docker(c):
    c.run("sh develop/docker-bash", pty=True)


@task
def setup(c):
    print("Installing requirements...")
    c.run("pip install -r requirements.txt -r requirements-dev.txt", hide=True)


@task
def test(c):
    c.run("python -m pytest -x tests/")


@task
def test_only(c, filter: str):
    c.run(f"python -m pytest -x -v -s -k {filter}")


@task
def cover(c):
    c.run("python -m pytest -x --cov-report term-missing --cov=twinfiles tests")


@task
def cover_only(c, filter: str):
    c.run(
        f"python -m pytest -x --cov-report term-missing --cov=twinfiles tests -k {filter}",
        pty=True,
    )
