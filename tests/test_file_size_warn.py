"""file-size-warn.py — M3: the warning must actually reach Claude.

PostToolUse stdout on exit 0 goes only to the debug transcript; the original
hook printed there unconditionally, so the >600-line warning was never seen.
The fix: exit 2 + stderr on breach, silence otherwise.
"""
import io
import json


def _event(path) -> io.StringIO:
    return io.StringIO(json.dumps({"tool_input": {"file_path": str(path)}}))


def test_over_limit_warns_stderr_exit_2(tmp_path, capsys, file_size_warn):
    md = tmp_path / "big.md"
    md.write_text("x\n" * 601)
    assert file_size_warn.main(_event(md)) == 2
    captured = capsys.readouterr()
    assert "big.md: 601 lines" in captured.err
    assert captured.out == ""


def test_at_limit_silent_exit_0(tmp_path, capsys, file_size_warn):
    md = tmp_path / "ok.md"
    md.write_text("x\n" * 600)
    assert file_size_warn.main(_event(md)) == 0
    captured = capsys.readouterr()
    assert captured.err == "" and captured.out == ""


def test_non_md_and_garbage_are_silent_exit_0(tmp_path, file_size_warn):
    py = tmp_path / "big.py"
    py.write_text("x\n" * 601)
    assert file_size_warn.main(_event(py)) == 0
    assert file_size_warn.main(io.StringIO("not json")) == 0
