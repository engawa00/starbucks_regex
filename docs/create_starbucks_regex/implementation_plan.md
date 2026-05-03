# 実装計画: StarbucksJP-Order-Regex

## 目的
日本のスターバックスのレギュラードリンクメニュー（カスタマイズ含む）を解析する正規表現を構築し、GUIアプリケーション、テスト、およびGitHub Actionsを備えたプロジェクトとして実装・公開する。

## User Review Required
> [!IMPORTANT]
> プロジェクトの正式名称として **StarbucksJP-Order-Regex** を提案します。
> この名前でよろしいでしょうか？（リポジトリ名やREADMEのタイトルに使用します）

## Open Questions
特にありませんが、GUIアプリケーションの動作イメージなどにご要望があればお知らせください。

## 提案される変更内容

### ドキュメント & 設定ファイル
#### [MODIFY] [README.md](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/README.md)
以下の内容を含むように更新します：
- プロジェクト名 (StarbucksJP-Order-Regex) と説明、特徴
- 動作要件 (Python 3.x, tkinter, pytest)
- 使い方 (GUIモードでの起動方法、Pythonからの直接利用方法)
- 開発者向け情報 (pytestの実行方法)
- 免責事項 (Disclaimer) とライセンス (MIT) の記載

#### [NEW] [pytest.yml](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/.github/workflows/pytest.yml)
- GitHub Actions上で `pytest` を自動実行するためのCI設定ファイルを作成します。

#### [MODIFY] [.gitignore](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/.gitignore)
- 既存の標準的な設定に加えて、必要であれば追記を行いますが、現状ですでに十分に網羅的であるため、大きな変更は行いません。

---

### Python実装
#### [NEW] [starbucks_regex.py](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/starbucks_regex.py)
- モジュールの先頭で指定された正規表現を定数 `STARBUCKS_DRINK_REGEX` として定義します。
- 受け取った文字列がメニューにマッチするかどうかを判定するヘルパー関数 `match_drink_order(order_str)` を実装します。

#### [NEW] [app.py](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/app.py)
- `tkinter` を使用したシンプルなGUIアプリケーション。
- テキストボックスに注文内容（例: "トール エクストラホイップ チョコチップ ダークモカチップフラペチーノ"）を入力し、「判定」ボタンを押すと、正規表現でのマッチ結果（マッチした部分、全体の妥当性など）を画面に表示します。

---

### テスト
#### [NEW] [test_starbucks_regex.py](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/tests/test_starbucks_regex.py)
- `pytest` を用いたテストコード。
- 正常系（様々なサイズの指定、カスタマイズの有無、ホット/アイスの指定など）および異常系（メニューにない文字列、不正な形式など）のケースを網羅します。

## 検証計画

### Automated Tests
- ローカルにて `pytest tests/test_starbucks_regex.py` を実行し、すべてのテストがパスすることを確認します。

### Manual Verification
- `python app.py` を実行してGUIアプリを起動し、いくつかの入力を手動で行い、正常に判定結果が表示されることを確認します。
