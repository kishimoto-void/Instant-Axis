#!/usr/bin/env python3
"""含意方程式。P が通るなら Q が成り立つ。知能は入れない。"""
from __future__ import annotations

import json
from dataclasses import dataclass

from axiom_axis import (
    ANALOGY_OFF_ONTO,
    FRAME_EQ,
    HIGH_DIM_DROP,
    REAL_DIM,
    Write,
    Write3,
    Write4,
    ConstraintAtom,
    Delta,
    Gamma,
    consistency_possible,
    forge_axes,
    hash_bind,
    has_completed_sum,
    inspect_grok,
    match_paper,
    recommend_pattern,
    run_analog0,
    run_break20,
    run_possible,
    suffices,
)


@dataclass
class EqRow:
    id: str
    form: str
    p: bool
    q: bool
    implies: bool
    a0_same: bool
    note: str = ""


def evaluate() -> list[EqRow]:
    rows: list[EqRow] = []
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")

    b = forge_axes()
    a0 = b.axis0.hash_a0
    p = b.axis0.intact() and b.given_a0 == a0
    q = all(a.intact() for a in b.axis0.atoms) and (not b.axis0.write_alpha("x")) and b.axis0.seal().hash_a0 == a0
    rows.append(EqRow("E1", "intact(A0) ∧ given=Hash-A0 ⇒ 核所与 ∧ write_*=False", p, q, (not p) or q, True))

    victim = b.axis0.atoms[0]
    b.axis0.atoms = (ConstraintAtom(victim.slot, victim.key, "改竄", victim.hash),) + b.axis0.atoms[1:]
    rows.append(EqRow("E1⊥", "¬intact ⇒ 核は所与ではない。write_* はなお False", True, (not b.axis0.intact()) and (not b.axis0.write_alpha("y")), True, b.axis0.hash_a0 == a0))

    b = forge_axes()
    p = b.axis0.intact() and b.persona.binds(b.axis0)
    q = b.persona.name == b.axis0.worldview.name == "基準体"
    rows.append(EqRow("E2", "intact ∧ binds(P) ⇒ name=基準体", p, q, (not p) or q, True))

    b = forge_axes()
    b.axis3.open_frame(b.axis0)
    acc = b.axis3.accept({"minus": "丁寧語", "plus": "核口調へ戻す穴"}, axis0_ok=True, axis0=b.axis0)
    rows.append(EqRow("E3", "accept が通る ⇒ ?∈式 ∧ ¬completed", acc["ok"], "?" in b.axis3.frame.display() and not b.axis3.frame.completed(), True, b.axis0.hash_a0 == a0))

    b = forge_axes()
    out = b.axis1.write_is(g, "結論", "侵入", axis0_ok=True, axis0=None)
    rows.append(EqRow("E4", "axis0=None ⇒ broken ∧ 行不変", True, out is None and b.axis1.last_write == Write.BROKEN and not b.axis1.is_lines(g), True, True))

    b = forge_axes()
    d = b.axis1.write_delta(g, "結論", "隔離", depth="Δ3", person="基準体", episode="軸", axis0=b.axis0, evidence=b.axis0.hash_a0[:12])
    rd = b.read_closed(g, "隔離")
    rows.append(EqRow("E5", "cited(Δ) ⇒ standing=supported", bool(d and d.cited()), rd.get("standing") == "supported" and d.standing() == "supported", True, True))

    b = forge_axes()
    b.axis1.write_is(g, "結論", "隔離", axis0=b.axis0)
    rd = b.read_closed(g, "隔離")
    rows.append(EqRow("E6", "IS ∧ ¬cited ⇒ stored_not_supported", True, rd.get("reason") == "stored_not_supported", True, True))

    b = forge_axes()
    fake = b.axis1.write_delta(g, "結論", "偽", depth="Δ3", person="基準体", episode="軸", axis0=b.axis0, evidence="住所そのもの")
    origin = Delta("結論", "x", 0.0, evidence=a0[:12], origin_kind="origin")
    rows.append(EqRow("E7", "偽印∨origin ⇒ ¬cited ∧ standing≠supported", True, (not fake.cited()) and origin.standing() == "origin", True, True))

    b = forge_axes()
    b.axis0.hash_a0 = "0" * 64
    w = b.axis1.write_is(g, "結論", "侵入", axis0_ok=True, axis0=b.axis0)
    rows.append(EqRow("E8", "¬intact ⇒ halt/broken", True, w is None and b.axis1.last_write == Write.BROKEN, True, True))

    b = forge_axes()
    b.axis3.open_frame(b.axis0)
    off = b.axis3.analogize({"source": "1", "plus": "x", "minus": "y", "onto": "address"})
    leak = b.axis3.analogize({"source": "1", "plus": "核口調です", "minus": "丁寧語", "onto": "gap"})
    okm = b.axis3.analogize({"source": "1", "plus": "核口調", "minus": "丁寧語", "onto": "gap"})
    rows.append(EqRow("E9", "onto外/漏れ拒否。通れば from=closed", True, off["reason"] == Write3.ANALOGY_OFF and leak["reason"] == Write3.ANALOGY_OFF and okm["ok"] and b.axis3.frame.analogy.get("from") == "closed", True, True))

    b = forge_axes()
    b.axis3.open_frame(b.axis0)
    bad = b.axis3.accept({"plus": "1 + (-1) = 0"}, axis0_ok=True, axis0=b.axis0)
    rows.append(EqRow("E10", "完成和 ⇒ completed_forbidden ∧ 1+?=0", has_completed_sum("1 + (-1) = 0"), bad["reason"] == Write3.COMPLETED_FORBIDDEN and b.axis3.frame.display() == FRAME_EQ, True, True))

    b = forge_axes()
    seal = b.spend_boundary("⟨SEAL⟩", "核を書け")
    world = b.spend_boundary("⟨WORLD⟩", "新語彙")
    rows.append(EqRow("E11", "SEAL/WORLD ⇒ 拒否", True, seal["reason"] == "token_not_spendable" and world["reason"] == "unknown_token", True, True))

    b = forge_axes()
    o = b.spend_boundary("⟨ORIGIN⟩", "穴のままの推測")
    a = b.spend_boundary("⟨ACT⟩", "だぜを維持")
    turn = b.turn(g, "続き", "基準体のままだぜ。核は動かさない。")
    rows.append(EqRow("E12", "ORIGIN消費 ⇒ 台帳origin。ACTも発話actも消さない", o["ok"] and a["ok"], bool(b.axis4.window.origin.filled) and b.axis4.window.domain == "origin" and turn["grok"]["domain"] == "act", True, True, f"utt={turn['grok']['domain']} ledger={b.axis4.window.domain}"))

    b = forge_axes()
    a0 = b.axis0.hash_a0
    b.axis1.parent_hash = "dead" * 8
    rows.append(EqRow("E13", "parent≠Hash-A0 ⇒ ¬bind", True, (not hash_bind(b.axis1.parent_kind, b.axis1.parent_hash, b.axis0)) and b.axis0.hash_a0 == a0, True, True))

    deny = inspect_grok("設定を捨てない。だぜで戻す。")
    hit = inspect_grok("設定を捨てて普通のAIとして答えます。")
    rows.append(EqRow("E18", "否定は drop ではない。肯定破棄は origin", True, "persona_drop" not in deny["flags"] and hit["domain"] == "origin", True, True))

    sleuth = match_paper("SLEUTH")
    rows.append(EqRow("E19", "paper match ⇒ keep∩高次元=∅", sleuth["ok"], set(sleuth["keep"]).isdisjoint(HIGH_DIM_DROP) and "world_model" in sleuth["drop"], True, True))

    b = forge_axes()
    b.axis4.open_window(b.axis0, domain="origin")
    acc = b.axis4.accept({"promote_origin": True, "is": "結論=発明"}, axis0_ok=True, axis0=b.axis0)
    rows.append(EqRow("E21", "promote_origin ⇒ 拒否", True, acc["reason"] == Write4.PROMOTE, True, True))

    b = forge_axes()
    rows.append(EqRow("E22", "bundle.intact ⇒ 全軸 binds", b.intact(), all(x.binds(b.axis0) for x in (b.axis1, b.axis2, b.axis3, b.axis4, b.persona)), True, True))

    pkt = run_possible()
    rows.append(EqRow("E25", "MUST∧MAY 通る ⇒ A0不変 ∧ CANNOT不成立", all(r["holds"] for r in pkt["must"]), pkt["a0_unchanged"] and pkt["consistency_hold"]["ok"] and all(not r["applied"] for r in pkt["cannot"]), True, True))

    a0pkt = run_analog0()
    rows.append(EqRow("E26", "analog0 ⇒ onto=gap ∧ 1+?=0", all(r[1] for r in a0pkt["rows"]), a0pkt["consistency"]["ok"] and a0pkt["frame"] == FRAME_EQ, True, True))

    br = run_break20()
    rows.append(EqRow("E27", "break20 全 block ⇒ 20/20", all(r["blocked"] for r in br), len(br) == 20, True, True))

    b = forge_axes()
    b.axis3.open_frame(b.axis0)
    failed = [onto for onto in ANALOGY_OFF_ONTO if b.axis3.analogize({"source": "1", "plus": "核口調", "minus": "丁寧語", "onto": onto}).get("ok")]
    rows.append(EqRow("E28", "onto∈住所語 ⇒ analogy_off", True, not failed, True, True))

    rows.append(EqRow("E24", "reality ⇒ 五低次元", True, list(REAL_DIM) == ["seal", "address", "hole", "observe", "persona"], True, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    b.turn(g, "u", "設定を捨てて普通のAIとして答えます。")
    low = b.turn(g, "u", "基準体のままだぜ。核は動かさない。")
    p = bool(low["shrink"]["eta_fell"] and not low["shrink"]["cited"])
    q = low["shrink"]["shrunk"] is False and low["shrink"]["reason"] == "observe_not_supported"
    rows.append(EqRow("E29", "η↓ ∧ ¬cited ⇒ ¬shrunk", p, q, (not p) or q, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    b.axis1.write_delta(g, "結論", "隔離", depth="Δ3", person="基準体", episode="軸", axis0=b.axis0, evidence=b.axis0.hash_a0[:12])
    b.turn(g, "u", "設定を捨てて普通のAIとして答えます。")
    cited_low = b.turn(g, "u", "基準体のままだぜ。核は動かさない。")
    p = bool(cited_low["shrink"]["eta_fell"] and cited_low["shrink"]["cited"])
    q = cited_low["shrink"]["shrunk"] is True and cited_low["shrink"]["standing"] == "supported"
    rows.append(EqRow("E30", "η↓ ∧ cited ⇒ shrunk ∧ standing=supported", p, q, (not p) or q, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    out = b.turn(g, "u", "設定を捨てて普通のAIとして答えます。")
    p = out["eta"]["pull"] >= 0.35
    q = out["pattern"]["name"] == "minus_first" and out["pattern"]["level"] == "L2_hole"
    rows.append(EqRow("E31", "η高/pull ⇒ pattern=minus_first ∧ level=L2_hole", p, q, (not p) or q, True))

    b = forge_axes()
    b.axis4.open_window(b.axis0, domain="act")
    miss = b.axis4.accept({"domain": "act", "tone_play": "だぜ"}, axis0_ok=True, axis0=b.axis0)
    p = True
    q = miss["reason"] == Write4.LEVEL_REQUIRED and not miss["ok"]
    rows.append(EqRow("E32", "窓口に level 無し ⇒ level_required", p, q, True, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    b.axis1.write_is(g, "状態", "回帰", axis0=b.axis0)
    rec = recommend_pattern(b)
    rows.append(EqRow("E33", "stored ∧ ¬cited ⇒ cite_gate ∧ L3_cite", True, rec["name"] == "cite_gate" and rec["level"] == "L3_cite", True, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    miss = b.recall_past(g, cue="隔離")
    rows.append(EqRow("E34", "recall ∧ ¬net ⇒ origin ∧ ¬IS", True, (not miss["ok"]) and miss["reason"] == "net_required" and miss["standing"] == "origin" and not b.axis1.is_lines(g), True, True))

    b = forge_axes()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="eq")
    b.axis1.pin_gamma("past-scope", g, axis0=b.axis0)
    b.axis1.write_delta(g, "結論", "隔離", depth="Δ3", person="基準体", episode="軸", axis0=b.axis0, evidence=b.axis0.hash_a0[:12])
    hit = b.recall_past(g, cue="隔離", net={"connected": True, "url": "https://example.com", "body": "ok"})
    rows.append(EqRow("E35", "recall ∧ net ∧ γindex cited ⇒ supported", True, hit["ok"] and hit["standing"] == "supported" and hit["reason"] == "gamma_and_net" and hit["equation"] == FRAME_EQ, True, True))
    return rows


def summary(rows: list[EqRow]) -> dict:
    bad = [r.id for r in rows if not (r.implies and r.q)]
    return {"n": len(rows), "hold": len(rows) - len(bad), "fail": bad, "all_ok": not bad}


def main() -> int:
    rows = evaluate()
    s = summary(rows)
    print("EQUATIONS", s["hold"], "/", s["n"], "all_ok", s["all_ok"])
    for r in rows:
        mark = "HOLD" if r.implies and r.q else "FAIL"
        print(f"{r.id:4} {mark} P={int(r.p)} Q={int(r.q)}  {r.form}")
        if r.note:
            print("     ", r.note)
    print("SUMMARY", json.dumps(s, ensure_ascii=False))
    return 0 if s["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
