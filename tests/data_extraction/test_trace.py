from pathlib import Path
from lean_dojo import *
from lean_dojo.data_extraction.cache import cache
from lean_dojo.utils import working_directory
from lean_dojo.data_extraction.lean import url_to_repo
from git import Repo


def test_github_trace(lean4_example_url):
    # github
    github_repo = LeanGitRepo(lean4_example_url, "main")
    assert github_repo.repo_type == "github"
    trace_repo = trace(github_repo)
    path = cache.get(github_repo.format_dirname / github_repo.name)
    assert path is not None


def test_remote_trace(remote_example_url):
    # remote
    remote_repo = LeanGitRepo(remote_example_url, "main")
    assert remote_repo.repo_type == "remote"
    trace_repo = trace(remote_repo)
    path = cache.get(remote_repo.format_dirname / remote_repo.name)
    assert path is not None


def test_local_trace(lean4_example_url):
    # local
    with working_directory() as tmp_dir:
        # git repo placed in `tmp_dir / repo_name`
        Repo.clone_from(lean4_example_url, "lean4-example")
        local_dir = str((tmp_dir / "lean4-example"))
        local_url = str((tmp_dir / "lean4-example").absolute())
        local_repo = LeanGitRepo(local_dir, "main")
        assert local_repo.url == local_url
        assert local_repo.repo_type == "local"
        trace_repo = trace(local_repo)
        path = cache.get(local_repo.format_dirname / local_repo.name)
        assert path is not None


def test_trace(traced_repo):
    traced_repo.check_sanity()


def test_get_traced_repo_path(mathlib4_repo):
    path = get_traced_repo_path(mathlib4_repo)
    assert isinstance(path, Path) and path.exists()
