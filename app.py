import tkinter as tk
from tkinter import messagebox
from starbucks_regex import STARBUCKS_JP_DRINK_MENU_REGEX, match_drink_order, extract_drink_order, _compiled_regex
import re

class StarbucksRegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Starbucks(JP) Drink Menu Regex Checker")
        self.root.geometry("600x450")
        self.root.configure(bg="#f2f0eb")

        frame = tk.Frame(self.root, padx=20, pady=20, bg="#f2f0eb")
        frame.pack(expand=True, fill=tk.BOTH)

        title_label = tk.Label(frame, text="☕ 日本のスターバックス 注文判定アプリ", font=("Helvetica", 16, "bold"), bg="#f2f0eb", fg="#00704a")
        title_label.pack(pady=(0, 20))

        entry_label = tk.Label(frame, text="注文内容を入力 (例: トール エクストラホイップ ダークモカチップフラペチーノ):", font=("Helvetica", 10), bg="#f2f0eb")
        entry_label.pack(anchor=tk.W)

        self.entry = tk.Entry(frame, width=70, font=("Helvetica", 14))
        self.entry.pack(pady=10)
        self.entry.insert(0, "トール エクストラホイップ ダークモカチップフラペチーノ")

        button = tk.Button(frame, text="判定する", command=self.evaluate_order, font=("Helvetica", 12, "bold"), bg="#00704A", fg="white", padx=10, pady=5)
        button.pack(pady=10)

        self.result_label = tk.Label(frame, text="", justify=tk.LEFT, font=("Helvetica", 11), bg="#ffffff", anchor="nw", relief=tk.SOLID, bd=1, padx=10, pady=10)
        self.result_label.pack(expand=True, fill=tk.BOTH, pady=10)

    def evaluate_order(self):
        order_str = self.entry.get().strip()
        if not order_str:
            messagebox.showwarning("警告", "注文内容を入力してください。")
            return

        is_full_match = match_drink_order(order_str)
        extracted = extract_drink_order(order_str)

        result_text = f"入力文字列: {order_str}\n\n"
        if is_full_match:
            result_text += "判定: 🟢 注文として完全にマッチしました！\n"
        elif extracted:
            result_text += f"判定: 🟡 部分的にマッチしました。\n抽出された注文: {extracted}\n"
        else:
            result_text += "判定: 🔴 マッチしませんでした。\n"

        # 正規表現のグループ詳細を表示
        match = _compiled_regex.search(order_str)
        if match:
            result_text += "\n--- マッチ詳細 ---\n"
            # 全てのグループを取得して、Noneでないものを表示
            for i, group in enumerate(match.groups(), start=1):
                if group:
                    result_text += f"グループ {i}: {group.strip()}\n"

        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = StarbucksRegexApp(root)
    root.mainloop()
