# 実装計画: 正規表現の柔軟性向上（スペース許容とシロップ追加）

## 目的
日本のスターバックスのドリンク注文において、単語間のスペースの有無に関わらずマッチするように正規表現を改善し、さらに主要なシロップの種類を個別に認識できるように追加します。

## 提案される変更内容

### [MODIFY] [starbucks_regex.py](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/starbucks_regex.py)
- `STARBUCKS_JP_DRINK_MENU_REGEX` の更新。
- **スペースの許容**:
    - ドリンク名（例: `スターバックス ラテ` -> `スターバックス\s?ラテ`）
    - カスタマイズ名（例: `アーモンドミルク` -> `アーモンド\s?ミルク`、`チョコチップ` -> `チョコ\s?チップ`）
- **シロップ種類の追加**:
    - 以下のシロップを個別に追加：
        - バニラシロップ
        - キャラメルシロップ
        - チョコレートシロップ
        - ホワイトモカシロップ
        - タゾチャイシロップ
        - アーモンドトフィーシロップ
        - クラシックシロップ
    - これらもスペースの有無（例: `バニラ シロップ`）に対応。

### [MODIFY] [tests/test_starbucks_regex.py](file:///c:/Users/n_e_e/OneDrive/Documents/GitHub/starbucks_regex/tests/test_starbucks_regex.py)
- 新しいパターンを確認するためのテストケースを追加：
    - スペースなしのドリンク名（例: `スターバックスラテ`）
    - スペースありのカスタマイズ（例: `チョコ チップ`）
    - 新しく追加したシロップ（例: `バニラシロップ追加`）

## 検証計画

### Automated Tests
- `pytest tests/test_starbucks_regex.py` を実行し、既存のテストと新規追加したテストがすべてパスすることを確認します。

### Manual Verification
- `app.py` を起動し、スペースを入れたり抜いたりした注文（例: `トールバニラシロップ追加スターバックスラテ`）が正しく認識されるか確認します。
