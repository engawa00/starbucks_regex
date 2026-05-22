import pytest
import zipfile
from unittest.mock import MagicMock
import release

def test_create_release_zip(monkeypatch, tmp_path):
    # Setup test variables
    test_version = "test-0.0.1"
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: test_version)

    # Use tmp_path to avoid modifying the real file system
    monkeypatch.setattr(release, '__file__', str(tmp_path / "release.py"))

    # Create dummy files so the release packager thinks they exist
    for f in release.FILES_TO_INCLUDE:
        (tmp_path / f).write_text(f"dummy content for {f}")

    expected_zip_path = tmp_path / f"starbucks_regex_{test_version}.zip"

    # Run the target function
    release.create_release_zip()

    # Verify the ZIP file was created in the correct location
    assert expected_zip_path.exists(), f"Expected ZIP file at {expected_zip_path} was not found"

    # Verify the ZIP file contents
    with zipfile.ZipFile(expected_zip_path, 'r') as zipf:
        zip_contents = zipf.namelist()
        assert "app.py" in zip_contents
        assert "starbucks_regex.py" in zip_contents
        assert "LICENSE" in zip_contents
        assert "README.md" in zip_contents
        assert len(zip_contents) == 4 # Ensure exactly 4 files are included

def test_create_release_zip_invalid_version(monkeypatch, tmp_path):
    # ../1.0 is invalid due to path traversal characters
    test_version = "../1.0"
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: test_version)

    # Mock print to verify it gets called
    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    monkeypatch.setattr(release, '__file__', str(tmp_path / "release.py"))
    zip_files_before = list(tmp_path.glob("*.zip"))

    release.create_release_zip()

    # Check for error message
    mock_print.assert_any_call("エラー: 不正なバージョン番号です。英数字、ドット(.)、ハイフン(-)のみ使用できます。")

    # Verify no new ZIP files were created
    zip_files_after = list(tmp_path.glob("*.zip"))
    assert len(zip_files_before) == len(zip_files_after)

@pytest.mark.parametrize("empty_val", ["", "   ", "\t", "\n"])
def test_create_release_zip_empty_version(monkeypatch, empty_val):
    # Empty string should be handled
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: empty_val)

    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    release.create_release_zip()

    # Check for error message
    mock_print.assert_any_call("エラー: バージョン番号が入力されませんでした。")

def test_create_release_zip_missing_files(monkeypatch, tmp_path):
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: "0.0.1")

    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    monkeypatch.setattr(release, '__file__', str(tmp_path / "release.py"))

    # Create all but 'LICENSE'
    for f in release.FILES_TO_INCLUDE:
        if f != 'LICENSE':
            (tmp_path / f).write_text(f"dummy content for {f}")

    release.create_release_zip()

    # Check for error message
    mock_print.assert_any_call("エラー: 以下の必須ファイルが見つかりません: LICENSE")
    mock_print.assert_any_call("リリース用ZIPの作成を中止します。")

def test_create_release_zip_exception(monkeypatch, tmp_path):
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: "0.0.1")

    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    monkeypatch.setattr(release, '__file__', str(tmp_path / "release.py"))

    # Create dummy files
    for f in release.FILES_TO_INCLUDE:
        (tmp_path / f).write_text(f"dummy content for {f}")

    # Force an exception when creating the zip file
    def raise_exception(*args, **kwargs):
        raise Exception("Test Exception")

    monkeypatch.setattr(zipfile, 'ZipFile', raise_exception)

    release.create_release_zip()

    # Check for error message
    mock_print.assert_any_call("\nエラー: ZIPファイルの作成中にエラーが発生しました: Test Exception")

def test_create_release_zip_multiple_missing_files(monkeypatch, tmp_path):
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: "0.0.1")

    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    monkeypatch.setattr(release, '__file__', str(tmp_path / "release.py"))

    # Create all but 'LICENSE' and 'README.md'
    for f in release.FILES_TO_INCLUDE:
        if f not in ['LICENSE', 'README.md']:
            (tmp_path / f).write_text(f"dummy content for {f}")

    release.create_release_zip()

    # Check for error message that includes both missing files
    mock_print.assert_any_call("エラー: 以下の必須ファイルが見つかりません: LICENSE, README.md")
    mock_print.assert_any_call("リリース用ZIPの作成を中止します。")
