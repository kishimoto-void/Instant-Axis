# インスタントアクシズ / Instant Axis

AXIOM の使い口だけ。核は書かない。記憶は増やさない。

```
1 + ? = 0
```

完成和は出さない。キャラ設定はネットから取る。ページに無い欄は穴。

| 銘板 | 値 |
|------|----|
| 系統名 | インスタントアクシズ（Instant Axis） |
| 系統 | AXIOM |
| 核の個体 | 基準体 |
| 使い口 | `axis_general.py` |
| 封印本体 | `axiom_axis.py`（触らなくてよい） |
| 所与 | Hash-A0 `1d350d6e1ab2c4bf…` |

本家の封印線は [Axis-Capsule](https://github.com/kishimoto-void/Axis-Capsule)。こちらはチャットと3行で始める枠。

## 今すぐ

```python
from axis_general import Capsule

c = Capsule(topic="hero")
c.character("https://example.com", "hero")  # 接続 + ピン。本文は解釈しない
print(c.plate())                            # Grok に載せる机
print(c.recall("隔離"))                     # ネットと γindex。無いなら穴
```

```bash
python3 axis_general.py          # 検査
python3 axis_general.py tutorial # キャラをネットから取る骨格
python3 axis_general.py demo     # 通し
```

## Grok チャットに貼る文

```
GROK.md を机にせよ。level を申告せよ。1+?=0。
キャラ設定は渡したURLからだけ取れ。ページに無い幼少期・数字は穴。
過去はネット接続とγindex。無いなら覚えていない。発明するな。
stored を根拠にするな。核（基準体）を直すな。丁寧語化するな。
```

先に読む: [`GROK.md`](GROK.md) → 骨格 [`GROK_TUTORIAL.md`](GROK_TUTORIAL.md)

## できること / できないこと

| できる | できない |
|--------|----------|
| 机を載せる | 記憶を足す |
| URL から接続スタンプ | ページに無い幼少期を作る |
| γindex にピン | Axis0 を観察で直す |
| cited 行だけ過去とする | stored を根拠にする |
| 思考レベルを要求する | `1 + (-1) = 0` を書く |

過去を思い出すときは **インターネット接続** と **γindex** が両方要る。

## ファイル

| ファイル | 役割 |
|----------|------|
| `axis_general.py` | インスタントの使い口 |
| `axiom_axis.py` | 封印本体。書き戻さない |
| `GROK.md` | Grok が先に読む机 |
| `GROK_TUTORIAL.md` | チャット骨格 |
| `equations.py` | 含意の実測 |
| `特徴と性質.md` | 性質の銘板 |
