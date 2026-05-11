import tkinter as tk
from tkinter import messagebox, ttk
from starbucks_regex import get_drink_order_match

# UI Constants
BG_COLOR = "#f2f0eb"
PRIMARY_COLOR = "#00704a"
WHITE = "#ffffff"
FONT_FAMILY = "Helvetica"

class StarbucksRegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Starbucks(JP) Drink Menu Regex Checker")
        self.root.geometry("600x450")
        self.root.configure(bg=BG_COLOR)

        frame = tk.Frame(self.root, padx=20, pady=20, bg=BG_COLOR)
        frame.pack(expand=True, fill=tk.BOTH)

        title_label = tk.Label(frame, text="☕ 日本のスターバックス 注文判定アプリ", font=(FONT_FAMILY, 16, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR)
        title_label.pack(pady=(0, 20))

        entry_label = tk.Label(frame, text="注文内容を入力、またはリストから選択:", font=(FONT_FAMILY, 10), bg=BG_COLOR)
        entry_label.pack(anchor=tk.W)

        examples = [
            "トール エクストラホイップ ダークモカチップフラペチーノ",
            "ショート キャラメルシロップ ホイップ カフェミスト",
            "ショート リストレット バニラシロップ スターバックスラテ",
            "エスプレッソショット追加 キャラメルマキアート",
            "トール ライトシロップ ライトソース キャラメルマキアート アイス",
            "グランデ チャイ ティー ラテ ホット"
        ]

        self.entry = ttk.Combobox(frame, values=examples, width=70, font=(FONT_FAMILY, 14))
        self.entry.pack(pady=10)
        self.entry.insert(0, examples[0])
        self.entry.bind("<Return>", self.evaluate_order)
        self.entry.bind("<<ComboboxSelected>>", self.evaluate_order)

        button = tk.Button(frame, text="判定する", command=self.evaluate_order, font=(FONT_FAMILY, 12, "bold"), bg=PRIMARY_COLOR, fg=WHITE, padx=10, pady=5)
        button.pack(pady=10)

        self.result_label = tk.Label(frame, text="", justify=tk.LEFT, font=(FONT_FAMILY, 11), bg=WHITE, anchor="nw", relief=tk.SOLID, bd=1, padx=10, pady=10)
        self.result_label.pack(expand=True, fill=tk.BOTH, pady=10)

    def evaluate_order(self, event=None):
        order_str = self.entry.get().strip()
        if not order_str:
            messagebox.showwarning("警告", "注文内容を入力してください。")
            return

        # 正規表現の判定と詳細取得を一度に行う
        match = get_drink_order_match(order_str)

        result_parts = [f"入力文字列: {order_str}\n\n"]
        if match:
            extracted = match.group(0).strip()
            if extracted == order_str:
                result_parts.append("判定: 〇 注文として完全にマッチしました！\n")
            else:
                result_parts.append(f"判定: △ 部分的にマッチしました。\n抽出された注文: {extracted}\n")

            result_parts.append("\n--- マッチ詳細 ---\n")
            # 全てのグループを取得して、Noneでないものを表示
            for i, group in enumerate(match.groups(), start=1):
                if group:
                    result_parts.append(f"グループ {i}: {group.strip()}\n")
        else:
            result_parts.append("判定: ✕ マッチしませんでした。\n")

        self.result_label.config(text="".join(result_parts))

if __name__ == "__main__":
    root = tk.Tk()
    app = StarbucksRegexApp(root)
    root.mainloop()
