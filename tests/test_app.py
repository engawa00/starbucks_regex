import pytest
import tkinter as tk
from unittest.mock import patch
from app import StarbucksRegexApp

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def app(root):
    return StarbucksRegexApp(root)

def test_app_initialization(app):
    """正常系：アプリの初期化が正しく行われることのテスト"""
    assert app.root.title() == "Starbucks(JP) Drink Menu Regex Checker"
    assert "トール エクストラホイップ ダークモカチップフラペチーノ" in app.entry.get()
    assert app.result_label.cget("text") == ""

@patch("app.messagebox.showwarning")
def test_evaluate_order_empty(mock_showwarning, app):
    """異常系：注文内容が空の場合、警告が表示されることのテスト"""
    app.entry.delete(0, tk.END)
    app.evaluate_order()

    mock_showwarning.assert_called_once_with("警告", "注文内容を入力してください。")
    assert app.result_label.cget("text") == ""

@patch("app.messagebox.showwarning")
def test_evaluate_order_whitespace(mock_showwarning, app):
    """異常系：注文内容が半角スペースのみの場合、警告が表示されることのテスト"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "   ")
    app.evaluate_order()

    mock_showwarning.assert_called_once_with("警告", "注文内容を入力してください。")
    assert app.result_label.cget("text") == ""

def test_evaluate_order_full_match(app):
    """正常系：完全一致する注文のテスト"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "トール エクストラホイップ ダークモカチップフラペチーノ")
    app.evaluate_order()

    result_text = app.result_label.cget("text")
    assert "判定: 〇 注文として完全にマッチしました！" in result_text
    assert "グループ 1: トール" in result_text
    assert "グループ 3: エクストラホイップ" in result_text
    assert "グループ 6: ダークモカチップフラペチーノ" in result_text

def test_evaluate_order_partial_match(app):
    """正常系：部分一致する注文のテスト"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "美味しい トール エクストラホイップ ダークモカチップフラペチーノ を飲んだ")
    app.evaluate_order()

    result_text = app.result_label.cget("text")
    assert "判定: △ 部分的にマッチしました。" in result_text
    assert "抽出された注文: トール エクストラホイップ ダークモカチップフラペチーノ" in result_text
    assert "グループ 1: トール" in result_text

def test_evaluate_order_no_match(app):
    """異常系：マッチしない注文のテスト（惜しいがマッチしないケース）"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "メロン オブ メロン フラペチーノ")
    app.evaluate_order()

    result_text = app.result_label.cget("text")
    assert "判定: ✕ マッチしませんでした。" in result_text
    assert "グループ" not in result_text
