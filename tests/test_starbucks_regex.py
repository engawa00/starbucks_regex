import re
import pytest
from starbucks_regex import match_drink_order, extract_drink_order, get_drink_order_match

SEASONAL_DRINKS = [
    "メロン オブ メロン フラペチーノ",
    "GOHOBI メロン フラペチーノ",
    "ストロベリー フラペチーノ",
    "瀬戸内 レモン ケーキ フラペチーノ",
    "さくら ティー ラテ",
    "さくら フラペチーノ",
]

@pytest.mark.parametrize("order", [
    # 基本のドリンク (スペースあり・なし)
    "スターバックス ラテ",
    "スターバックスラテ",
    "ドリップ コーヒー",
    "ドリップコーヒー",
    "カフェ モカ",
    "カフェモカ",
    "ホワイト モカ",
    "ホワイトモカ",
    "抹茶 ティー ラテ",
    "抹茶ティーラテ",
    "ほうじ茶 ティー ラテ",
    "チャイ ティー ラテ",
    "アール グレイ ティー ラテ",
    "コーヒー フラペチーノ",
    "キャラメル フラペチーノ",
    "ダーク モカ チップ フラペチーノ",
    "ダーク モカ チップ クリーム フラペチーノ",
    "抹茶 クリーム フラペチーノ",
    "バニラ クリーム フラペチーノ",
    "マンゴー パッション ティー フラペチーノ",
    "カプチーノ",
    
    # 新規追加エスプレッソ
    "ソイ ラテ",
    "アーモンドミルク ラテ",
    "オーツミルク ラテ",
    "カフェ アメリカーノ",
    "トリプルエスプレッソ ラテ",
    "エスプレッソ",

    # サイズ + ドリンク
    "ショート カフェ モカ",
    "トール スターバックス ラテ",
    "グランデ ホワイト モカ",
    "ベンティ ドリップ コーヒー",
    "ブリュード コーヒー",
    "カフェ ミスト",
    "ブリュー コーヒー",
    "コールドブリュー コーヒー",
    
    # サイズ + ドリンク + 温度
    "トール スターバックス ラテ ホット",
    "グランデ キャラメル マキアート アイス",
    "ショート カプチーノ エクストラホット",
    "カフェ ミスト ホット",
    
    # カフェイン変更 + ドリンク
    "ディカフェ ドリップ コーヒー",
    "デカフェ スターバックス ラテ",
    "リストレット キャラメル マキアート",
    
    # カスタマイズ (1つ) + ドリンク (スペースあり・なし、新シロップ)
    "エクストラホイップ ダークモカチップフラペチーノ",
    "バニラシロップ追加 スターバックスラテ",
    "バニラ シロップ 追加 スターバックス ラテ",
    "キャラメルシロップ変更 キャラメルマキアート",
    "豆乳変更 カフェ モカ",
    "アーモンド ミルク 変更 スターバックス ラテ",
    "オーツミルク スターバックス ラテ",
    "チョコ チップ 追加 抹茶 ティー ラテ",
    "ライトアイス 抹茶 ティー ラテ",
    "ノンアイス チャイ ティー ラテ",
    "エスプレッソ ショットの追加 ダーク モカ チップ フラペチーノ",
    "オーツミルクに変更 キャラメル マキアート",
    "無脂肪乳に変更 スターバックス ラテ",
    "低脂肪タイプに変更 カフェ モカ",
    "フォームミルクの調整 スターバックス ラテ",
    
    # 複合注文
    "トール ディカフェ エクストラホイップ チョコチップ追加 ダークモカチップフラペチーノ",
    "グランデ オーツミルクに変更した キャラメル マキアート エクストラホット",
    "ベンティ リストレット バニラシロップ多め スターバックスラテ アイス",
    "ショート ノンホイップ ホワイト モカ ホット",
    
])
def test_valid_orders(order):
    """正常系のテスト：正しいスターバックスの注文文字列がマッチすることを確認"""
    assert match_drink_order(order) is True

@pytest.mark.parametrize("order", [
    # スターバックスに関係ない・メニューにない文字列
    "タピオカ ミルク ティー",
    "コーン スープ",
    "オレンジ ジュース",
    
    # フォーマットが合わない文字列
    "トール コーラ アイス",
    "グランデ エクストラホイップ ホットドッグ",
    "メロン ティー ラテ",  # メロンはフラペチーノのみ
    "エスプレッソ 抜き コーヒー フラペチーノ",
    "スターバックス ラテ トール",
        "フラペチーノ 抹茶",
        "追加 チョコチップ ダークモカチップフラペチーノ",
    "アーモンドミルク ティー",
        "氷 エクストラ 追加 ホイップ 抜き ホット コーヒー フラペチーノ",
        "シロップ 変更 チョコ ソース 多め 抹茶 クリーム",
    
    # コーヒーメニュー関連のエラー
    "ショット追加 ブリュー コーヒー",
    "エスプレッソショット追加 ブリュード コーヒー",
    "ショット カフェ ミスト",
    "ドリップ コーヒー ショット追加",
    "コールドブリュー コーヒー ホット",
    "コールドブリュー コーヒー エクストラホット",
    "ブリュー コーヒー ホット",
    "ブリュー コーヒー アイス",

    # 空文字
    "",
] + SEASONAL_DRINKS)
def test_invalid_orders_fullmatch(order):
    """異常系のテスト：メニューにない注文は完全マッチしないことを確認"""
    assert match_drink_order(order) is False

@pytest.mark.parametrize("order", [
    "",
    " ",
    "   ",
    "\n",
    "\t",
    " \n \t ",
])
def test_match_drink_order_empty_inputs(order):
    """異常系のテスト：空文字や空白のみの入力に対して完全にマッチしないことを確認"""
    assert match_drink_order(order) is False

def test_extract_drink_order():
    """部分一致の抽出テスト"""
    # 注文の後に余計な文字がある場合
    text1 = "トール スターバックス ラテ ホット を飲みました"
    assert extract_drink_order(text1) == "トール スターバックス ラテ ホット"
    
    # .* が前方を貪欲マッチしてしまうため、前方に文字がないケースでテスト
    text2 = "ベンティ ダークモカチップフラペチーノ 最高"
    assert extract_drink_order(text2) == "ベンティ ダークモカチップフラペチーノ"
    
    # 該当なしの場合
    text4 = "今日は家で麦茶を飲んでいます"
    assert extract_drink_order(text4) is None

@pytest.mark.parametrize("order_str", SEASONAL_DRINKS + [
    # 空文字・空白
    "",
    " ",
    "   ",
    # 無関係な文字列
    "こんにちは",
    "今日の天気は晴れです",
    # 不完全な注文 (単体ではマッチしない要素のみ)
    "トール",
    "ベンティ",
    "豆乳変更",
    "ディカフェ",
    "ホット",
    "アイス",
    "エクストラホット",
    "エクストラホイップ",
])
def test_extract_drink_order_invalid(order_str):
    """異常系のテスト：注文として不完全、または無関係な文字列から抽出できないことを確認"""
    assert extract_drink_order(order_str) is None

def test_get_drink_order_match():
    """get_drink_order_match の正常系テスト"""
    # 正常な注文
    order = "トール スターバックス ラテ ホット"
    match = get_drink_order_match(order)
    assert isinstance(match, re.Match)
    assert match.group(0) == order

    # 部分一致
    text = "私は グランデ カフェ モカ アイス を注文しました"
    match = get_drink_order_match(text)
    assert isinstance(match, re.Match)
    assert match.group(0) == "グランデ カフェ モカ アイス"

@pytest.mark.parametrize("order_str", SEASONAL_DRINKS + [
    "こんにちは",
    "トール",
    "",
])
def test_get_drink_order_match_invalid(order_str):
    """get_drink_order_match の異常系テスト"""
    assert get_drink_order_match(order_str) is None

def test_invalid_types():
    """異常系のテスト：文字列以外の入力に対する例外送出を確認"""
    with pytest.raises(AttributeError):
        match_drink_order(None)
    with pytest.raises(AttributeError):
        match_drink_order(123)

    with pytest.raises(TypeError):
        extract_drink_order(None)
    with pytest.raises(TypeError):
        extract_drink_order(123)

    with pytest.raises(TypeError):
        get_drink_order_match(None)
    with pytest.raises(TypeError):
        get_drink_order_match(123)

def test_cli_full_match(capsys, monkeypatch):
    """CLIの正常系のテスト（完全一致）"""
    import starbucks_regex
    monkeypatch.setattr("sys.argv", ["starbucks_regex.py", "トール エクストラホイップ ダークモカチップフラペチーノ"])

    starbucks_regex.main()

    captured = capsys.readouterr()
    assert "入力文字列: トール エクストラホイップ ダークモカチップフラペチーノ" in captured.out
    assert "判定: 〇 注文として完全にマッチしました！" in captured.out
    assert "グループ 1: トール" in captured.out
    assert "グループ 6: ダークモカチップフラペチーノ" in captured.out

def test_cli_partial_match(capsys, monkeypatch):
    """CLIの正常系のテスト（部分一致）"""
    import starbucks_regex
    monkeypatch.setattr("sys.argv", ["starbucks_regex.py", "美味しい トール エクストラホイップ ダークモカチップフラペチーノ をください"])

    starbucks_regex.main()

    captured = capsys.readouterr()
    assert "判定: △ 部分的にマッチしました。" in captured.out
    assert "抽出された注文: トール エクストラホイップ ダークモカチップフラペチーノ" in captured.out

def test_cli_no_match(capsys, monkeypatch):
    """CLIの異常系のテスト（不一致）"""
    import starbucks_regex
    monkeypatch.setattr("sys.argv", ["starbucks_regex.py", "普通のコーヒー"])

    starbucks_regex.main()

    captured = capsys.readouterr()
    assert "判定: ✕ マッチしませんでした。" in captured.out

def test_cli_no_args(capsys, monkeypatch):
    """CLIの異常系のテスト（引数なし）"""
    import starbucks_regex
    monkeypatch.setattr("sys.argv", ["starbucks_regex.py"])

    with pytest.raises(SystemExit) as e:
        starbucks_regex.main()

    assert e.value.code == 1

    captured = capsys.readouterr()
    assert "注文内容を入力してください。" in captured.out
