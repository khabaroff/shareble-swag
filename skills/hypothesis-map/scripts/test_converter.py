"""Self-check: python3 test_converter.py (exit 0 = ok)."""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
data = {
    "title": "Тест",
    "goal": {"description": 'Цоколь "чистый"\nвсегда',
             "metrics": [{"name": "Загрязнения", "current": "10/день", "target": 0}],
             "balancing": [{"name": "Конфликты", "current": "0", "target": "0"}]},
    "subjects": [{"name": "Владельцы собак", "pains_desires": ["Боюсь за собаку"],
                  "hypotheses": [{"if": "мы повесим надпись", "then": "обходят цоколь",
                                  "because": "боятся за питомца", "result": "загрязнения → 0",
                                  "priority": "high", "tasks": ["Текст", "Разместить"]}]}],
}
with tempfile.TemporaryDirectory() as d:
    src, out = os.path.join(d, "map.json"), os.path.join(d, "карта.excalidraw")
    with open(src, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(HERE, "excalidraw_converter.py"), src, out], check=True)
    with open(out, encoding="utf-8") as f:
        doc = json.load(f)
    assert doc["type"] == "excalidraw"
    ids = {e["id"] for e in doc["elements"]}
    arrows = [e for e in doc["elements"] if e["type"] == "arrow"]
    assert len(arrows) == 4, len(arrows)  # 2 task→hyp, hyp→subj, subj→goal
    assert all(a["startBinding"]["elementId"] in ids and a["endBinding"]["elementId"] in ids for a in arrows)
    assert any('"чистый"' in e.get("text", "") for e in doc["elements"])
print("ok")
