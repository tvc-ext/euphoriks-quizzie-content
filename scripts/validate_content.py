import json
from collections import Counter
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())
assert manifest["schemaVersion"] == 1
assert manifest["questionCount"] >= 900
ids = set()
total = 0
for entry in manifest["packs"]:
    path = Path(entry["path"])
    assert path.exists(), path
    data = json.loads(path.read_text())
    if entry["type"] != "questions":
        continue
    questions = data["questions"]
    assert len(questions) == 100, path
    total += len(questions)
    prompts = set()
    levels = set()
    concepts = []
    for question in questions:
        assert question["id"] not in ids
        ids.add(question["id"])
        assert question["prompt"] not in prompts
        prompts.add(question["prompt"])
        assert len(question["options"]) >= 3
        assert 0 <= question["correctIndex"] < len(question["options"])
        assert question["explanation"].strip()
        assert question["difficulty"] in {"easy", "medium", "hard"}
        levels.add(question["difficulty"])
        concepts.append(question["conceptId"])
    assert levels == {"easy", "medium", "hard"}
    concept_counts = Counter(concepts)
    assert len(concept_counts) >= 25, (path, len(concept_counts))
    assert max(concept_counts.values()) <= 4, (path, concept_counts.most_common(1))
assert total == manifest["questionCount"]
print(f"Validated {total} questions across {len(manifest['packs']) - 1} topic packs")
