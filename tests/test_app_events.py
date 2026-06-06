import pytest
import tkinter as tk

def test_entry_bind_combobox_selected(app):
    """正常系：Comboboxの選択イベント(<<ComboboxSelected>>)が正しく処理されることのテスト"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "ショート カフェミスト")
    app.result_label.config(text="")

    app.entry.event_generate("<<ComboboxSelected>>")
    app.root.update()

    result_text = app.result_label.cget("text")
    assert "判定: 〇 注文として完全にマッチしました！" in result_text

def test_entry_bind_return(app):
    """正常系：EntryのEnterキー入力(<Return>)が正しく処理されることのテスト"""
    app.entry.delete(0, tk.END)
    app.entry.insert(0, "ショート カフェミスト")
    app.result_label.config(text="")

    # 仮想環境(Xvfb)等でイベントを確実に発火させるため、フォーカスを当ててからupdateを挟む
    app.entry.focus_force()
    app.root.update()
    app.entry.event_generate("<Return>")
    app.root.update()

    result_text = app.result_label.cget("text")
    assert "判定: 〇 注文として完全にマッチしました！" in result_text
