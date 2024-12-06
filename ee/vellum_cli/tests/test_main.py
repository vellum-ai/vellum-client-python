import subprocess


def test_cli__root():
    """
    A test sanity ensuring that the CLI is accessible
    """

    result = subprocess.run(["vellum", "--help"], capture_output=True)
    assert result.returncode == 0
    assert result.stdout.startswith(b"Usage: vellum")
