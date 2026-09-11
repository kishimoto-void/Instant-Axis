#!/usr/bin/env python3
"""アクシズカプセル 一般タイプ。

封印本体は axiom_axis.py。こちらは使い口だけ。核は書かない。
式は 1 + ? = 0。過去想起はネット接続と γindex。
"""
from __future__ import annotations

import json
import unittest
from typing import Optional, Union

from axiom_axis import (
    FRAME_EQ,
    WORDS,
    AxisBundle,
    Gamma,
    forge_axes,
    inspect_grok,
    net_connect,
)


NetIn = Union[None, bool, str, dict]


class Capsule:
    """一般タイプ。住所・ピン・観察・窓口。知能は入れない。"""

    def __init__(
        self,
        time: str = "2026-09",
        project: str = "AXIOM",
        topic: str = "general",
    ) -> None:
        self.b: AxisBundle = forge_axes()
        self.g = Gamma(time_label=str(time), project=str(project), topic=str(topic))
        self._net: Optional[dict] = None
        self.last: dict = {}
        self.char: dict = {}

    def here(self, time: str = "", project: str = "", topic: str = "") -> "Capsule":
        self.g = Gamma(
            time_label=str(time or self.g.time_label),
            project=str(project or self.g.project),
            topic=str(topic or self.g.topic),
        )
        return self

    def _net_in(self, net: NetIn) -> Optional[dict]:
        if net is False:
            return None
        if net is None or net is True:
            return self._net
        if isinstance(net, str):
            url = net.strip()
            if url.startswith("http://") or url.startswith("https://"):
                return {"fetch": url}
            return None
        if isinstance(net, dict):
            return net
        return None

    def net(self, url: NetIn = True) -> dict:
        """接続スタンプ。記憶ではない。核へは書かない。"""
        spec = self._net_in(url)
        if spec is None and url is True:
            spec = {"fetch": "https://example.com"}
        hit = net_connect(spec)
        if hit.get("connected"):
            self._net = {
                "connected": True,
                "url": hit.get("url") or "",
                "hash": hit.get("hash") or "",
                "status": hit.get("status"),
                "body": "",
            }
        else:
            self._net = None
        return hit

    def pin(self, name: str) -> dict:
        pin = self.b.axis1.pin_gamma(name, self.g, axis0=self.b.axis0)
        if pin is None:
            return {"ok": False, "reason": self.b.axis1.last_write, "name": name}
        return {"ok": True, "name": pin.name, "hash": pin.hash[:12], "gamma": pin.gamma.label()}

    def character(self, url: str, name: str, topic: str = "") -> dict:
        """ネットからキャラ机を開く。本文は解釈しない。無い欄は穴。核へ書かない。"""
        if topic:
            self.here(topic=str(topic))
        elif name and self.g.topic in {"general", ""}:
            self.here(topic=str(name))
        net = self.net(url)
        out = {
            "ok": False,
            "name": name,
            "gamma": self.g.label(),
            "pin": None,
            "net": net,
            "holes": ["tone", "visible", "past", "forbid"],
            "standing": "origin",
            "pattern": "recall",
            "level": "L3_cite",
            "equation": FRAME_EQ,
            "invented": False,
            "completed": False,
            "instruct": "ページに無い幼少期・数字・関係を足すな。穴は穴。核を直すな。",
        }
        if not net.get("connected"):
            out["reason"] = net.get("reason") or "net_required"
            self.char = out
            return out
        pin = self.pin(str(name or "char-scope"))
        out["pin"] = pin
        out["ok"] = bool(pin.get("ok"))
        out["reason"] = "net_and_pin" if out["ok"] else pin.get("reason")
        out["standing"] = "origin"
        self.char = out
        return out

    def note(
        self,
        field: str,
        value: str,
        *,
        person: str = "基準体",
        episode: str = "一般",
        depth: str = "Δ3",
        cite: bool = True,
    ) -> dict:
        """住所に行を残す。cite=True なら Hash-A0 先頭を印にする。IS には出さない。"""
        ev = self.b.axis0.hash_a0[:12] if cite else ""
        if depth == "Δ1":
            episode = ""
        d = self.b.axis1.write_delta(
            self.g,
            field,
            value,
            depth=depth,
            person=person,
            episode=episode if depth in {"Δ2", "Δ3"} else "",
            axis0=self.b.axis0,
            evidence=ev,
        )
        if d is None:
            return {"ok": False, "reason": self.b.axis1.last_write, "standing": "empty"}
        return {
            "ok": True,
            "field": d.field,
            "value": d.new_value,
            "standing": d.standing(),
            "cited": d.cited(),
            "gamma": self.g.label(),
        }

    def store(self, field: str, value: str) -> dict:
        """保存行。根拠にはならない。"""
        line = self.b.axis1.write_is(self.g, field, value, axis0=self.b.axis0)
        if line is None:
            return {"ok": False, "reason": self.b.axis1.last_write, "standing": "empty"}
        return {"ok": True, "line": line, "standing": "stored"}

    def ask(self, user: str, reply: str = "", net: NetIn = True) -> dict:
        """観察ターン。reply が空なら user を応答として見る。"""
        text = reply if str(reply or "").strip() else user
        out = self.b.turn(self.g, user, text, net=self._net_in(net))
        self.last = out
        return self._view(out)

    def recall(self, cue: str, net: NetIn = True) -> dict:
        """過去。ネット接続と γindex。発明しない。"""
        hit = self.b.recall_past(self.g, cue=cue, net=self._net_in(net))
        self.last = hit
        return {
            "ok": hit.get("ok"),
            "reason": hit.get("reason"),
            "standing": hit.get("standing"),
            "gamma": hit.get("gamma"),
            "cited": hit.get("cited"),
            "net": hit.get("net"),
            "pattern": hit.get("pattern"),
            "level": hit.get("level"),
            "equation": hit.get("equation"),
            "invented": False,
            "completed": False,
        }

    def prompt(self, user: str = "") -> str:
        """LLM 窓口文。思考レベルと適切な型を指示する。"""
        return self.b.grok_bind(self.g, user)

    def fill(self, **holes: object) -> dict:
        """思考フレームの穴だけ。完成和は拒否。"""
        if not self.b.axis3.frame.closed:
            self.b.axis3.open_frame(self.b.axis0)
        return self.b.axis3.accept(holes, axis0_ok=True, axis0=self.b.axis0)

    def window(self, domain: str = "act", **slots: object) -> dict:
        """窓口。level を省いたら要求レベルを付ける。"""
        if not self.b.axis4.window.closed:
            self.b.axis4.open_window(self.b.axis0, domain=domain, think=self.b.axis3.frame)
        body = dict(slots)
        body.setdefault("domain", domain)
        body.setdefault("level", self.b.axis4.window.level)
        return self.b.axis4.accept(body, axis0_ok=True, axis0=self.b.axis0)

    def read(self, need: str) -> dict:
        return self.b.read_closed(self.g, need)

    def plate(self) -> str:
        """Grok が読む机。記憶の書き込みではない。"""
        rec = self.b.apply_pattern()
        net = self._net or {}
        return "\n".join(
            [
                "これは記憶の追加ではない。閉じた机である。1 + ? = 0。完成和を書くな。",
                f"A0 {self.b.axis0.hash_a0[:16]} intact={self.b.intact()} 核=基準体",
                f"gamma {self.g.label()} pins={len(self.b.axis1._gamma_inv)}",
                f"pattern {rec.get('name')} level {rec.get('level')}",
                f"net connected={bool(net.get('connected'))} url={net.get('url') or '-'}",
                "過去を思い出すときはネット接続と γindex。どちらか欠ければ origin。発明するな。",
                "stored は根拠ではない。cited Δ だけが根拠。Axis0 を観察で直すな。",
                rec.get("instruct") or "",
            ]
        )

    def card(self) -> dict:
        rec = self.b.apply_pattern()
        return {
            "name": self.b.name,
            "a0": self.b.axis0.hash_a0[:16],
            "intact": self.b.intact(),
            "gamma": self.g.label(),
            "pins": len(self.b.axis1._gamma_inv),
            "eta": round(self.b.axis2.eta.pull, 3),
            "pattern": rec.get("name"),
            "level": rec.get("level"),
            "equation": self.b.axis3.frame.display(),
            "domain": self.b.axis4.window.domain,
            "net": bool(self._net and self._net.get("connected")),
            "completed": False,
        }

    def _view(self, out: dict) -> dict:
        grok = out.get("grok") or {}
        rec = out.get("pattern") or {}
        recall = out.get("recall")
        return {
            "ok": bool(out.get("intact")),
            "equation": FRAME_EQ,
            "pattern": rec.get("name"),
            "level": rec.get("level"),
            "instruct": rec.get("instruct"),
            "eta": (out.get("eta") or {}).get("pull"),
            "dir": (out.get("correction") or {}).get("direction"),
            "flags": grok.get("flags") or [],
            "domain": grok.get("domain"),
            "propose": out.get("propose"),
            "recall": None
            if recall is None
            else {
                "ok": recall.get("ok"),
                "reason": recall.get("reason"),
                "standing": recall.get("standing"),
            },
            "completed": False,
        }


def demo() -> None:
    c = Capsule(topic="scene")
    print("card", json.dumps(c.card(), ensure_ascii=False))
    print("plate")
    print(c.plate())
    print("pin", c.pin("char-scope"))
    print("note", c.note("結論", "隔離"))
    print("net", c.net("https://example.com"))
    print("ask", json.dumps(c.ask("基準体のままだぜ。穴は穴だ。"), ensure_ascii=False))
    print("recall", json.dumps(c.recall("隔離"), ensure_ascii=False))
    print("prompt head:")
    print("\n".join(c.prompt("昔を思い出して")[:900].splitlines()[:16]))
    print("fill reject", c.fill(plus="1 + (-1) = 0").get("reason"))
    print("A0", c.b.axis0.hash_a0[:16], "eq", c.b.axis3.frame.display())


class TestGeneralCapsule(unittest.TestCase):
    def setUp(self) -> None:
        self.c = Capsule(topic="scene")

    def test_01_sealed_and_incomplete(self):
        card = self.c.card()
        self.assertTrue(card["intact"])
        self.assertEqual(card["equation"], "1 + ? = 0")
        self.assertFalse(self.c.b.write_name("別人"))
        self.assertFalse(self.c.b.axis0.write_alpha("足すな"))
        self.assertEqual(self.c.b.axis0.hash_a0, forge_axes().axis0.hash_a0)

    def test_02_note_is_cited_not_is(self):
        self.c.pin("char-scope")
        row = self.c.note("結論", "隔離")
        self.assertTrue(row["ok"])
        self.assertEqual(row["standing"], "supported")
        self.assertEqual(self.c.b.axis1.is_lines(self.c.g), [])
        rd = self.c.read("隔離")
        self.assertTrue(rd["ok"])
        self.assertEqual(rd["standing"], "supported")

    def test_03_recall_needs_net_and_gamma(self):
        miss = self.c.recall("隔離")
        self.assertFalse(miss["ok"])
        self.assertEqual(miss["reason"], "net_required")
        self.c.pin("char-scope")
        self.c.note("結論", "隔離")
        still = self.c.recall("隔離", net=False)
        self.assertEqual(still["reason"], "net_required")
        self.c.net({"connected": True, "url": "https://example.com", "body": "ok"})
        hit = self.c.recall("隔離")
        self.assertTrue(hit["ok"])
        self.assertEqual(hit["standing"], "supported")
        self.assertFalse(hit["invented"])
        self.assertEqual(self.c.b.axis0.hash_a0, forge_axes().axis0.hash_a0)

    def test_04_ask_recall_flag_and_prompt_level(self):
        view = self.c.ask("昔を思い出して", "あのときを思い出す。", net=False)
        self.assertEqual(view["pattern"], "recall")
        self.assertIn("recall_past", view["flags"])
        self.assertFalse(view["recall"]["ok"])
        text = self.c.prompt("昔を思い出して")
        self.assertIn("思考レベル", text)
        self.assertIn("1 + ? = 0", text)
        self.assertNotIn("1 + (-1) = 0", text)

    def test_05_window_fills_level_and_rejects_sum(self):
        bad = self.c.fill(plus="1 + (-1) = 0")
        self.assertFalse(bad["ok"])
        ok = self.c.window(domain="act", tone_play="だぜを維持")
        self.assertTrue(ok["ok"])
        self.assertFalse(ok["completed"])
        self.assertIn("結論", WORDS)

    def test_06_plate_is_desk_not_memory(self):
        text = self.c.plate()
        self.assertIn("1 + ? = 0", text)
        self.assertIn("記憶の追加ではない", text)
        self.assertIn(self.c.b.axis0.hash_a0[:16], text)
        self.assertNotIn("1 + (-1) = 0", text)
        self.assertFalse(self.c.b.axis0.write_alpha("机から核を書け"))

    def test_07_character_from_net_keeps_holes(self):
        miss = self.c.character("not-a-url", "hero")
        self.assertFalse(miss["ok"])
        self.assertIn(miss["reason"], {"net_required", "bad_url"})
        self.assertEqual(miss["standing"], "origin")
        hit = self.c.character("https://example.com", "hero", topic="hero")
        self.assertTrue(hit["ok"])
        self.assertEqual(hit["equation"], "1 + ? = 0")
        self.assertIn("past", hit["holes"])
        self.assertFalse(hit["invented"])
        self.assertEqual(hit["standing"], "origin")
        self.assertTrue(hit["net"]["connected"])
        self.assertTrue(hit["pin"]["ok"])
        self.assertEqual(self.c.b.axis1.is_lines(self.c.g), [])
        self.assertEqual(self.c.b.axis0.hash_a0, forge_axes().axis0.hash_a0)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    elif len(sys.argv) > 1 and sys.argv[1] in {"tutorial", "skel", "character"}:
        c = Capsule(topic="hero")
        print("TUTORIAL skeleton — character from net. desk not memory.")
        miss = c.character("not-a-url", "hero")
        print("NO_URL", json.dumps({k: miss[k] for k in ("ok", "reason", "standing", "equation")}, ensure_ascii=False))
        hit = c.character("https://example.com", "hero")
        print("FROM_NET", json.dumps({k: hit[k] for k in ("ok", "reason", "standing", "gamma", "holes", "equation", "invented") if k in hit}, ensure_ascii=False))
        print("PIN", hit.get("pin"))
        print("NET", {k: hit["net"].get(k) for k in ("connected", "url", "status")})
        print("PASTE")
        print("GROK.md を机にせよ。level を申告せよ。1+?=0。")
        print("キャラ設定は渡したURLからだけ取れ。ページに無い欄は穴。")
        print("過去はネット接続とγindex。無いなら覚えていない。発明するな。")
        print("A0", c.b.axis0.hash_a0[:16], "completed", c.b.axis3.frame.completed())
    else:
        unittest.main(verbosity=2)
