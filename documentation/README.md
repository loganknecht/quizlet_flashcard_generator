# quizlet_flashcard_generator
Used to simplify and create a comprehension method for flashcard Japanese flash card generation

# Environment Configuration
- Install Python
    - `brew install python`

# Repository Configuration
- Configure `virtualenv` for Python 3
- Activate virtualenv
- Install dependencies
    - You'll want everything, so use the dev dependencies
    - `pip install -r source/requirements.txt`
- Install pykakasi

# Running
You **MUST** make sure that the `output_directory` specified exists

- `python source_code/flashcard_generator.py --help`

- Generate flashcards
```
python source_code/flashcard_generator.py \
    --i ./input_directory/私立先生 \
    --o ./output_directory/私立先生
```

- The output will have the `\n\n` used as a delimter for the card contents
- The output will have the `==` used as a delimter for the term on the left and the definition on the right
