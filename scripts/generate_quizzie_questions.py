import json
from collections import Counter
from pathlib import Path

AGE_BANDS = ["explorer6to8", "adventurer9to11", "creator12to14"]
SOURCE_DIR = Path("source")
OUTPUT_DIR = Path("questions")


def difficulty_for(index: int, variant: int) -> str:
    if index < 8:
        base = 0
    elif index < 18:
        base = 1
    else:
        base = 2
    return ("easy", "medium", "hard")[min(2, max(base, variant // 2))]


def question_from_fact(topic_id: str, fact: list[str], index: int, variant: int) -> dict:
    concept_id, prompt, answer, wrong1, wrong2, explanation = fact
    concept_label = concept_id.replace("_", " ")

    prompts = [
        prompt,
        f"Which answer best fits this clue: {prompt}",
        f"Quizzie challenge: choose the correct statement for {concept_label}.",
        f"If you were teaching a friend about {concept_label}, which answer would you use?",
    ]
    options = [
        [answer, wrong1, wrong2],
        [wrong1, answer, wrong2],
        [wrong1, wrong2, answer],
        [answer, wrong2, wrong1],
    ]
    correct_indices = [0, 1, 2, 0]

    return {
        "id": f"{topic_id}.{concept_id}.q{variant}",
        "conceptId": concept_id,
        "prompt": prompts[variant],
        "options": options[variant],
        "correctIndex": correct_indices[variant],
        "explanation": explanation,
        "difficulty": difficulty_for(index, variant),
        "ageBands": AGE_BANDS,
    }


def generate_pack(source_path: Path) -> tuple[Path, dict]:
    source = json.loads(source_path.read_text(encoding="utf-8"))
    topic_id = source["topicId"]
    facts = source["facts"]
    if len(facts) != 25:
        raise ValueError(f"{source_path}: expected exactly 25 distinct concepts, got {len(facts)}")

    concept_ids = [fact[0] for fact in facts]
    if len(set(concept_ids)) != len(concept_ids):
        raise ValueError(f"{source_path}: duplicate concept ids")

    questions = [
        question_from_fact(topic_id, fact, index, variant)
        for index, fact in enumerate(facts)
        for variant in range(4)
    ]

    if len(questions) != 100:
        raise AssertionError(f"{topic_id}: expected 100 generated questions")
    if len({q["prompt"] for q in questions}) != 100:
        raise ValueError(f"{topic_id}: generated prompts are not unique")
    counts = Counter(q["conceptId"] for q in questions)
    if max(counts.values()) != 4:
        raise ValueError(f"{topic_id}: unexpected concept repetition")

    pack = {
        "schemaVersion": 1,
        "packVersion": 3,
        "topicId": topic_id,
        "questionCount": len(questions),
        "questions": questions,
    }
    return OUTPUT_DIR / f"{topic_id}.v1.json", pack


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(SOURCE_DIR.glob("*.json"))
    if len(sources) != 9:
        raise ValueError(f"Expected 9 topic source files, found {len(sources)}")

    total = 0
    for source_path in sources:
        output_path, pack = generate_pack(source_path)
        output_path.write_text(
            json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        total += pack["questionCount"]
        print(f"Generated {pack['questionCount']} questions -> {output_path}")

    if total != 900:
        raise AssertionError(f"Expected 900 questions, generated {total}")
    print(f"Generated {total} questions across {len(sources)} topics")


if __name__ == "__main__":
    main()
