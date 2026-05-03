# Walkthrough: StarbucksJP-Drink-Menu-Regex

## 達成したこと
日本のスターバックスのレギュラードリンクメニュー（カスタマイズ含む）を解析する正規表現を用いて、以下のコンポーネントを実装し、GitHubでの公開準備を整えました。

- **`starbucks_regex.py`**:
  - 指定された正規表現を定数 `STARBUCKS_JP_DRINK_MENU_REGEX` に格納。
  - 注文文字列の完全一致判定関数 `match_drink_order()` と、部分一致抽出関数 `extract_drink_order()` を実装。
- **`app.py`**:
  - `tkinter` を用いたGUIアプリケーションを実装。
  - テキストボックスに注文を入力し、「判定する」ボタンでマッチ結果と正規表現のグループ詳細を確認できるUIを構築。
- **`tests/test_starbucks_regex.py`**:
  - `pytest` による自動テストを作成。
  - サイズ、カスタマイズ、温度変更など複数の正常系パターンおよび異常系パターンを網羅。すべてパスすることを確認済み。
- **`.github/workflows/pytest.yml`**:
  - GitHubにプッシュした際、あるいはプルリクエスト時に自動で `pytest` が実行されるように設定。
- **`README.md`**:
  - プロジェクトの特徴、動作要件、実行方法（GUI/CLI）、テスト実行方法を記載。
  - 末尾に指定された免責事項とMITライセンスの記述を追加。

## 検証結果
- ローカル環境にて `pytest` を実行し、**30件のテストがすべて成功**（`30 passed`）することを確認しました。
- 正規表現における貪欲なマッチ(`.*`)に関する考慮など、テストケース内で適切に検証を行っています。

## その他
ユーザーからのご要望通り、プロジェクトタイトルと定数名の整合性をとるため、定数を `STARBUCKS_JP_DRINK_MENU_REGEX` に変更しています。
また、作成した各種ドキュメント（`task.md`, `implementation_plan.md`, `walkthrough.md`）は `docs/create_starbucks_regex/` フォルダへ保存しました。
