# Euphoriks Quizzie Content

Public, read-only learning packs for the Euphoriks Quizzie kids app.

- No child profiles, analytics, names, photos, or other user data.
- Versioned JSON packs are downloaded and cached by the app.
- Built-in app content remains available offline.
- Each quiz topic contains 100 prompts across at least 25 distinct learning concepts.
- Questions are tagged easy, medium, or hard.
- Images remain hosted by their credited public sources.

Content must pass the JSON validation workflow before merging. Generated questions should be fact-checked and sampled by a human reviewer.

## Question-pack source

The `source/` directory contains reviewed topic facts. `scripts/generate_quizzie_questions.py` deterministically turns 25 distinct facts per topic into 100 age-band-compatible question prompts. Validation prevents a shallow bank from masquerading as a large one by requiring at least 25 concepts and no more than four questions per concept.

## License

Original Euphoriks Quizzie question and game content: CC BY-SA 4.0. Third-party material retains its stated source license.
