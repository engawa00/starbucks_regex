import re
import argparse
import sys

# 日本のスターバックスのレギュラードリンクメニュー（カスタマイズ含む）にマッチする正規表現
# ※プロジェクト名と整合性を取るため、定数名を STARBUCKS_JP_DRINK_MENU_REGEX としています。
STARBUCKS_JP_DRINK_MENU_REGEX = (
    r"(?i)"
    r"(?:"
        r"(?:"
            r"(ショート|トール|グランデ|ベンティ)?\s?"
            r"(?:(ディカフェ|デカフェ|リストレット)\s?(?:に\s?変更)?)?\s?"
            r"(?="
                r"("
                    r"(?:"
                        r"(?:ライト|エクストラ|ノン)?\s?"
                        r"(?:"
                            r"(?!アーモンド\s?ミルク\s?ラテ|オーツ\s?ミルク\s?ラテ|ソイ\s?ラテ|エスプレッソ(?!\s?ショット)|コーヒー\s?フラペチーノ|ミルク\s?コーヒー|カフェ\s?ミスト|キャラメル\s?クリーム)"
                            r"(?:ホイップ(?:\s?クリーム)?|ムース\s?フォーム|豆乳|アーモンド\s?ミルク|オーツ\s?ミルク|低脂肪(?:タイプ|乳)?|無脂肪乳|ノンファット\s?ミルク|フォーム\s?ミルク|ミルク|"
                            r"バニラ(?:\s?フレーバー)?\s?シロップ|キャラメル(?:\s?フレーバー)?\s?シロップ|チョコ(?:レート)?\s?シロップ|ホワイト\s?モカ(?:\s?フレーバー)?\s?シロップ|タゾ\s?チャイ\s?シロップ|アーモンド\s?トフィー\s?シロップ|クラシック\s?シロップ|シロップ|"
                            r"チョコ(?:レート)?\s?ソース|キャラメル\s?ソース|ソース|"
                            r"チョコ(?:レート)?\s?チップ|シトラス\s?果肉|エスプレッソ\s?ショット|ショット|コーヒー|氷|ライト\s?アイス|エクストラ\s?アイス|ノン\s?アイス)"
                        r")\s?"
                        r"(?:に)?\s?(?:の)?\s?(?:追加|増量|変更|抜き|多め|少なめ|調整)?(?:した)?\s?"
                    r")*"
                r")"
            r")\3\s?"
            r"(?:"
                r"("
                    r"スターバックス\s?ラテ|ソイ\s?ラテ|アーモンド\s?ミルク\s?ラテ|オーツ\s?ミルク\s?ラテ|キャラメル\s?マキアート|カフェ\s?モカ|ホワイト\s?モカ|カフェ\s?アメリカーノ|トリプル\s?エスプレッソ\s?ラテ|"
                    r"(?:抹茶|ほうじ茶|チャイ|アール\s?グレイ|カモミール|ゼン\s?クラウド\s?ウーロン|イングリッシュ\s?ブレックファスト)\s?ティー\s?ラテ"
                r")\s?(ホット|アイス|エクストラホット)?"
                r"|"
                r"("
                    r"(?:コーヒー|エスプレッソ\s?アフォガート|キャラメル|ダーク\s?モカ\s?チップ(?:\s?クリーム)?|抹茶\s?クリーム|バニラ\s?クリーム|マンゴー\s?パッション\s?ティー)\s?フラペチーノ"
                r")\s?(アイス)?"
                r"|"
                r"(カプチーノ|エスプレッソ)\s?(ホット|エクストラホット)?"
            r")"
        r")"
        r"|"
        r"(?:"
            r"(ショート|トール|グランデ|ベンティ)?\s?"
            r"(?:(ディカフェ|デカフェ)\s?(?:に\s?変更)?)?\s?"
            r"(?="
                r"("
                    r"(?:"
                        r"(?:ライト|エクストラ|ノン)?\s?"
                        r"(?:"
                            r"(?!アーモンド\s?ミルク\s?ラテ|オーツ\s?ミルク\s?ラテ|ソイ\s?ラテ|エスプレッソ|コーヒー\s?フラペチーノ|ミルク\s?コーヒー|カフェ\s?ミスト|キャラメル\s?クリーム|ドリップ\s?コーヒー|ブリュード\s?コーヒー|ブリュー\s?コーヒー|コールドブリュー\s?コーヒー)"
                            r"(?:ホイップ(?:\s?クリーム)?|ムース\s?フォーム|豆乳|アーモンド\s?ミルク|オーツ\s?ミルク|低脂肪(?:タイプ|乳)?|無脂肪乳|ノンファット\s?ミルク|フォーム\s?ミルク|ミルク|"
                            r"バニラ(?:\s?フレーバー)?\s?シロップ|キャラメル(?:\s?フレーバー)?\s?シロップ|チョコ(?:レート)?\s?シロップ|ホワイト\s?モカ(?:\s?フレーバー)?\s?シロップ|タゾ\s?チャイ\s?シロップ|アーモンド\s?トフィー\s?シロップ|クラシック\s?シロップ|シロップ|"
                            r"チョコ(?:レート)?\s?ソース|キャラメル\s?ソース|ソース|"
                            r"チョコ(?:レート)?\s?チップ|シトラス\s?果肉|コーヒー|氷|ライト\s?アイス|エクストラ\s?アイス|ノン\s?アイス)"
                        r")\s?"
                        r"(?:に)?\s?(?:の)?\s?(?:追加|増量|変更|抜き|多め|少なめ|調整)?(?:した)?\s?"
                    r")*"
                r")"
            r")\12\s?"
            r"(?:"
                r"("
                    r"ドリップ\s?コーヒー|ブリュード\s?コーヒー|カフェ\s?ミスト"
                r")\s?(ホット|アイス|エクストラホット)?"
                r"|"
                r"(ブリュー\s?コーヒー|コールドブリュー\s?コーヒー)"
            r")"
        r")"
    r")"
)

_compiled_regex = re.compile(STARBUCKS_JP_DRINK_MENU_REGEX)

def match_drink_order(order_str: str) -> bool:
    """
    指定された注文文字列が、日本のスターバックスのドリンクメニュー（カスタマイズ含む）として
    全体が完全にマッチするかどうかを判定します。

    Args:
        order_str (str): 判定する注文文字列

    Returns:
        bool: 完全にマッチすれば True、そうでなければ False
    """
    order_str = order_str.strip()
    match = _compiled_regex.fullmatch(order_str)
    return match is not None

def extract_drink_order(order_str: str) -> str | None:
    """
    指定された文字列からスターバックスの注文部分を抽出します。
    部分一致で検索します。

    Args:
        order_str (str): 検索対象の文字列

    Returns:
        str | None: マッチした部分文字列。見つからない場合は None
    """
    match = _compiled_regex.search(order_str)
    if match:
        return match.group(0).strip()
    return None

def get_drink_order_match(order_str: str) -> re.Match | None:
    """
    指定された文字列からスターバックスの注文部分の Match オブジェクトを取得します。

    Args:
        order_str (str): 検索対象の文字列

    Returns:
        re.Match | None: マッチした場合は Match オブジェクト、見つからない場合は None
    """
    return _compiled_regex.search(order_str)


def main():
    parser = argparse.ArgumentParser(
        description="Starbucks(JP) Drink Menu Regex Checker CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    examples = [
        "トール エクストラホイップ ダークモカチップフラペチーノ",
        "ショート キャラメルシロップ ホイップ カフェミスト",
        "ショート リストレット バニラシロップ スターバックスラテ",
        "エスプレッソショット追加 キャラメルマキアート",
        "トール ライトシロップ ライトソース キャラメルマキアート アイス",
        "グランデ チャイ ティー ラテ ホット"
    ]
    examples_str = "\n".join(f"  '{ex}'" for ex in examples)

    parser.add_argument(
        "order",
        type=str,
        nargs="?",
        help=f"判定する注文文字列\n例:\n{examples_str}"
    )
    args = parser.parse_args()

    if not args.order or not args.order.strip():
        print("注文内容を入力してください。")
        print("使用例:")
        for ex in examples:
            print(f"  python starbucks_regex.py '{ex}'")
        sys.exit(1)

    order_str = args.order.strip()
    match = get_drink_order_match(order_str)

    print(f"入力文字列: {order_str}")
    print()

    if match:
        extracted = match.group(0).strip()
        if extracted == order_str:
            print("判定: 〇 注文として完全にマッチしました！")
        else:
            print("判定: △ 部分的にマッチしました。")
            print(f"抽出された注文: {extracted}")

        print()
        print("--- マッチ詳細 ---")
        for i, group in enumerate(match.groups(), start=1):
            if group:
                print(f"グループ {i}: {group.strip()}")
    else:
        print("判定: ✕ マッチしませんでした。")

if __name__ == "__main__":
    main()
