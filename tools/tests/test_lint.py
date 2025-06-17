from pathlib import Path
from tools import deno_lint


def test_lint():
    res, err = deno_lint.lint(Path("tests/App.tsx"))
    print(res)
    assert err is None
