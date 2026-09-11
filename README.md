# インスタントアクシズ / Instant Axis

AXIOM の使い口だけ。核は書かない。記憶は重みに足さない。強化は γindex。

```
1 + ? = 0
```

完成和は出さない。キャラ設定はネットから取る。ページに無い欄は穴。関係度は後で。

| 銘板 | 値 |
|------|----|
| 系統名 | インスタントアクシズ（Instant Axis） |
| 系統 | AXIOM |
| 核の個体 | 基準体 |
| 使い口 | `axis_general.py` |
| 封印本体 | `axiom_axis.py`（触らなくてよい） |
| 所与 | Hash-A0 `1d350d6e1ab2c4bf…` |

本家の封印線は [Axis-Capsule](https://github.com/kishimoto-void/Axis-Capsule)。こちらはチャットと数行で始める枠。

## 今すぐ

```python
from axis_general import Capsule

c = Capsule(topic="hero")
c.character("https://example.com", "hero")  # ネットからキャラ机
c.keep("結論", "隔離")                      # γindex で記憶強化
c.around()                                  # 周りを穴で開く（関係度は後で）
print(c.memory("隔離"))                     # 接続と γindex。無いなら穴
print(c.plate())
```

```bash
python3 axis_general.py          # 検査
python3 axis_general.py tutorial # ネット・γ・周りの骨格
python3 axis_general.py demo     # 通し
```

## 骨格

| 段 | 口 | すること | まだしない |
|----|----|----------|------------|
| 1 | `character(url, name)` | ネット接続 + ピン | 本文の発明 |
| 2 | `keep(field, value)` | 同じ住所に cited 行 | IS に出す |
| 3 | `around(url="")` | 場所・他者・小道具を穴で開く | 関係度 |
| 4 | `memory(cue)` | 接続 ∧ γindex で読む | 無い過去を作る |

関係度（親疎・距離）は後で追記する。今は `relation.later=True`。数字を付けるな。

## Grok チャットに貼る文

```
GROK.md を机にせよ。level を申告せよ。1+?=0。
キャラ設定は渡したURLからだけ取れ。ページに無い幼少期・数字は穴。
過去はネット接続とγindex。無いなら覚えていない。発明するな。
キャラのあと周りは穴で開け。関係度は後で。今は付けるな。
stored を根拠にするな。核（基準体）を直すな。丁寧語化するな。
```

先に読む: [`GROK.md`](GROK.md) → 骨格 [`GROK_TUTORIAL.md`](GROK_TUTORIAL.md)

## できること / できないこと

| できる | できない |
|--------|----------|
| URL からキャラ机を開く | ページに無い幼少期を作る |
| γindex で cited を残す | 重みの記憶を足したと称する |
| 周りを穴で開く | 関係度を今つける |
| 接続 ∧ γ で過去を読む | Axis0 を観察で直す |

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
