A good job for Generative AI is classifying text.

This is a code example of exactly how you can do this with OpenAI.

This example will:

1. Read in a lists of different types from the `hero.txt`, `location.txt`, and `subject.txt` files.
2. Process it using the instructions from the `system-prompt.txt` and `user-prompt.txt` file.
3. Use OpenAI to generate a story.
4. Output the results to the `results.txt` file.

Processing is done by running the commmand `python storytelling.py` or by running the `storytelling.py` file in a debugger.

__NOTES__

* All of the python code resides in the `storytelling.py` file and in the `workplace_common` library.
* Any of the configurations (API keys, etc. are handled automatically)

