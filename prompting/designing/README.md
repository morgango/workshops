A good job for Generative AI is  generating customized text.

This is a code example of exactly how you can do this with OpenAI.

These examples will:

1. Read parts of the prompt from input files:
   *  `length.txt`
   *  `location.txt`
   *  `mentions.txt`
   *  `nickname.txt`
   *  `shots.txt`
   *  `start.txt`
2. Process it using the instructions from the files:
   * `system-prompt.txt`
   * `user-prompt-simple.txt`
   * `user-prompt-refined.txt`
   * `user-prompt-complete.txt`
3. Use OpenAI to generate the text.
4. Output the results to the `results.txt` file.

Processing is done by running the commmand `designing-simple.py`, `desigining-refined.py`, or `designing-complete.py` in python or in a debugger.

__NOTES__

* All of the python code resides in the files `designing-simple.py`, `desigining-refined.py`, and `designing-complete.py` files and in the `workplace_common` library.
* Any of the configurations (API keys, etc. are handled automatically)

