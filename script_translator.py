import pandas as pd
import openai
import csv
openai.api_key = "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"

# Import CSV
def ImportCSV(ruta):
    print("### Import CSV function")
    try:
        df = pd.read_csv(ruta, delimiter="|",encoding='latin-1')
        return df
    except FileNotFoundError:
        return ("File not found.")
    


# Method to view csv's metadata
def analysis_csv(df):
    print("### CSV ANALYSIS")
    print(df.info())
    print("")
    # null_rows = df[df['english'].isnull()]
    # print("Nº rows with english = None", len(null_rows))



# Function to create the prompt to the OpenAI model
def create_example_list_translations(df):
    print("### Creating an example list of english literals")
    df1 = df.loc[df['english'].notnull(), 'english']
    df1.to_csv(PATH_PROMPTFILE_TXT, sep=' ', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar=' ')    


# Function to create the prompt to the OpenAI model
def create_prompt(df):
    print("### Creating Prompt")



# Function to do OpenAI API call 
def openAI_API_call():
    with open(PATH_PROMPTFILE_TXT, "r",encoding="latin-1") as file:
        print("\t ### Iniciando lectura del prompt ###")
        prompt = file.read()
        file.close()
    try:
        print("\t ### Initializing OpenAI API call ###")

        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            temperature=0.00000001,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        if response and response.choices:
            return response.choices[0].message['content'].encode('utf-8').decode('utf-8')
        else:
            print("\t ### The API response is empty.")
            return 1
    except openai.error.OpenAIError as e:
        print(f"Error with comunicating with API {e}")
        return 1
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return 1

    finally:
        print("\t ### API call completed ###")


# Function that writes the GPT response into resources/GPTresponse.txt
def save_raw_GPTresponse (response):
    print("\t ### Initializing raw response written into './resources/GPTresponse.txt' ###")
    with open("./resources/GPTresponse.txt", "w", encoding="utf-8") as file:
        file.write(response)
        file.close()


############################################################################
################################### MAIN ###################################
############################################################################

# File to be translated
PATH_TRANSLATION_CSV = "./translations v5.csv"
PATH_PROMPTFILE_TXT = "./resources/promptTranslations.txt"
if __name__ == "__main__":

    print("### MAIN ###")
    df = ImportCSV(PATH_TRANSLATION_CSV)

    if isinstance (df, pd.DataFrame):
        # If there is no error
        # Analysis of CSV dataframe
        analysis_csv(df)

        # create_example_list_translations(df)
        # create_prompt(df)
        response = openAI_API_call()
        
        save_raw_GPTresponse(response)

    else:
        print(df)

    print("### END ###")