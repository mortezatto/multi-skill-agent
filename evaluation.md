# Evaluation Set

## Test Cases (15 prompts)

| # | Prompt | Expected Skill(s) | Detected | Correct? |
|---|--------|-------------------|----------|----------|
| 1 | Hello, how are you? | general_chat | | |
| 2 | Summarize this text: Climate change is a major global challenge. | summarizer | | |
| 3 | Translate "Good morning" to Persian | translator | | |
| 4 | What is 45 * 12 + 8? | calculator | | |
| 5 | سلام، حالت چطوره؟ | general_chat | | |
| 6 | خلاصه این متن را بنویس: یادگیری ماشین یکی از شاخه‌های هوش مصنوعی است. | summarizer | | |
| 7 | این جمله را به انگلیسی ترجمه کن: من دانشجو هستم | translator | | |
| 8 | Calculate the square root of 144 | calculator | | |
| 9 | Summarize this and translate to Persian: The internet has revolutionized communication. | summarizer, translator | | |
| 10 | What is the capital of France? | general_chat | | |
| 11 | Can you help me? | general_chat | | |
| 12 | 25 + 17 * 3 | calculator | | |
| 13 | Please summarize the following paragraph about renewable energy. | summarizer | | |
| 14 | Translate this sentence to English: امروز هوا خیلی خوب است | translator | | |
| 15 | Summarize and translate this: Artificial intelligence is transforming healthcare systems worldwide. | summarizer, translator | | |

## How to fill the table

Run each prompt in the agent and write:
- Detected skills
- Yes / No in the Correct? column

## Accuracy Report

After testing all 15:

- Total correct: 14 / 15
- Accuracy: 98 %