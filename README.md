# Translator_GenerativeModel

## Summary
This script aims to address a specific task involving a file named "translations v5.csv". This file contains three columns relevant to the task: [english, portuguese, spanish]. The goal is to translate the literals in the "english" column into "portuguese" and "spanish". Rows that are already translated remain unchanged.

To accomplish the translations, the script makes calls to the OpenAI API, requiring an API_KEY with a paid plan. The default generative model used is **gpt-4-0613**, which provides higher translation quality. When calling the API, a prompt is constructed that includes the English literals mentioned earlier.

The simplified process of the script is as follows:
- First, the CSV file with the data is read. The path to this file is stored in the variable **PATH_TRANSLATION_CSV**.
- In the **"translation_generator"** function, groups of English literals to be translated are created. The number of elements in each group depends on the global variable **BATCH_ELEMENTS_PARAM** (default value is 50). This means that each API call returns translations for up to 50 rows from the CSV. Additionally, these groups exclude any rows that are already translated. 
- The prompt sent for each group to the API is written to a file named **"./resources/promptTranslations.txt"**. The generative model's response for each group is written to **"./resources/GPTresponse.txt"**. These files are useful for testing the script.
- Finally, the translations are added back to the **"translations v5.csv"** file.

## Important Script Parameters
- The **PATH** of the CSV file containing the input data can be modified in the global variable **PATH_TRANSLATION_CSV**.
- The number of translations per API call can be adjusted in the global variable **BATCH_ELEMENTS_PARAM**. By default, this is set to 50. It is not advisable to use a higher value, as the model may not return accurate responses.
- The number of groups of 50 literals to be translated can be changed in the global variable **N_GROUPS_PROCESSED**. The total number of groups derived from the "translations v5.csv" file can be substantial if there is a lot of data.

## Running the Script
It is essential to have Python installed along with the necessary libraries: **openai** and **chardet**. To install them, run:
```bash
pip install openai
pip install chardet

Additionally, you must configure an environment variable named "OPENAI_API_KEY" with your API KEY.

The script can be executed with the following command:
  ```bash
  python ./script_translator.py
  ```
## Conclusion
This script provides a streamlined approach to translating text using OpenAI's powerful language model while managing input and output via CSV files. It effectively ensures that already translated texts remain intact while processing new translations in batches.

## Example Output

```bash
#########################
### Iteration  0  ###
#########################

 ### Create_prompt function ###
 ### OpenAI_API_call function ###
 ### Initializing the reading of the prompt file ###
 ### Initializing OpenAI API call ###
 ### API call completed ###
 ### Initializing raw response written into './resources/GPTresponse.txt' function ###
 ### Initializing translations' UPDATE './resources/translations v5.csv' function ###

### Number of rows translated: 50 ###
### Iteration execution time: 56.85 seconds ###
### Total execution time: 56.85 seconds ###

#########################
### Iteration  1  ###
#########################

 ### Create_prompt function ###
 ### OpenAI_API_call function ###
 ### Initializing the reading of the prompt file ###
 ### Initializing OpenAI API call ###
 ### API call completed ###
 ### Initializing raw response written into './resources/GPTresponse.txt' function ###
 ### Initializing translations' UPDATE './resources/translations v5.csv' function ###

### Number of rows translated: 100 ###
### Iteration execution time: 73.47 seconds ###
### Total execution time: 130.32 seconds ###
