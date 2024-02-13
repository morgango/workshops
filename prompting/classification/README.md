A good job for Generative AI is classifying text.

This is a code example of exactly how you can do this with OpenAI.

This example will:

1. Read in a lists of different types from the `flowers-list.txt`, `people-list.txt`, and `food-list.txt` files.
2. Process it using the instructions from the `system-prompt.txt` file.
3. Use OpenAI to decide if this is a flower or a person.
4. Output the results to the `results-simple.txt` and `results-refined.txt` files.

Processing is done by running the commmand `classification-simple.py` or `classification-refined.py` file in python or a debugger.

__NOTES__

* All of the python code resides in the `classification-simple.py` or `classification-refined.py` files and in the `workplace_common` library.
* Any of the configurations (API keys, etc. are handled automatically)
* If you run this multiple times it will add the new text to the end of the `results-simple.txt` and `results-refined.txt` file.

