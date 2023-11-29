import pandas as pd
from openai import OpenAI
import chardet
import time


# Function to detect the encoding of csv file
def detect_encoding(path):
    print("### Encoding detection function ###")
    with open(path, 'rb') as f:
        result = chardet.detect(f.read())
    print("\t ### Encoding of CSV FILE: ", result['encoding'])
    return result['encoding']



# Import CSV file 
def ImportCSV(path, encoding):
    # print("### Import CSV function ###")
    try:
        df = pd.read_csv(path, delimiter="|", encoding=encoding)
        return df
    except FileNotFoundError:
        return ("File not found.")
    


# Method to view csv's metadata
def analysis_csv(df):
    print("### CSV ANALYSIS function ###")
    print(df.info())
    print("")
        # null_rows = df[df['english'].isnull()]
        # print("Nº rows with english = None", len(null_rows))



# Function to create the prompt to the OpenAI model
def create_prompt(df, encoding):
    print("\t ### Create_prompt function ###")
        ################# Example of df right now ###############
        #                                                     file                   object                    label                                            english portuguese spanish
        # 0  /jet-composites/alerts/notifications-list/reso...  root.notifications-list       workplace_reason_1  You have to change the requisites for the fina...        NaN     NaN
        # 2  /jet-composites/alerts/notifications-list/reso...  root.notifications-list       workplace_reason_3  {0} Director Manager requested {2} information...        NaN     NaN

    df1 = df[['english', 'portuguese', 'spanish']]
    df1.to_csv(PATH_PROMPTFILE_TXT, encoding=encoding, sep="|", index = True, header=True, index_label="index")  

    # Once we write the english data we want to be translated, we need to write the command at the beginning
    command_text = "Traduce los siguientes literales que estan en ingles a portugues y español. Devuelveme solo el csv, sin ninguna explicacion. El formato de salida debe ser un archivo con un estilo csv en el que haya cuatro columnas, la primera columna llamada index contiene los mismos indices de la consulta, la segunda es english, la tercera es portuguese y la cuarta es spanish. Aquellas traducciones que ya esten completas, no las traduzca. El separador tiene que ser |. La lista de literales a traducir es la siguiente:"

    with open(PATH_PROMPTFILE_TXT, 'r+',encoding=encoding) as file:
        original_content = file.read()
        file.seek(0)
        file.write(command_text)
        file.write('\n')
        file.write(original_content)
        file.close()



# Function that executes the OpenAI API call. Be careful if the openai Library gets updates. The way the call is done could be change.
def openAI_API_call(encoding):
    print("\t ### OpenAI_API_call function ###")

    with open(PATH_PROMPTFILE_TXT, "r",encoding=encoding) as file:
        print("\t ### Initializing the reading of the prompt file ###")
        prompt_ = file.read()
        file.close()

    
    try:
        print("\t ### Initializing OpenAI API call ###")
        chat_completion = client.chat.completions.create(model="gpt-4-0613", temperature=0.00000001, messages=[{"role": "user", "content": prompt_}])

        if chat_completion and chat_completion.choices:
            return chat_completion.choices[0].message.content
        else:
            print("\t ### The API response is empty.")
            return 1
    finally:
        print("\t ### API call completed ###")



# Function that writes the GPT response into resources/GPTresponse.txt
def save_raw_GPTresponse (response, encoding):
    print("\t ### Initializing raw response written into './resources/GPTresponse.txt' function ###")
    with open("./resources/GPTresponse.txt", "w", encoding=encoding) as file:
        file.write(response)
        file.close()



# Function that updates the translations v5.file with the batch translations received by GPT
def save_translations(df_aux, encoding):
    print("\t ### Initializing translations' UPDATE './resources/translations v5.csv' function ###")
    df_file = ImportCSV(PATH_TRANSLATION_CSV, encoding)

    df_file.loc[df_aux.index, ['english', 'spanish', 'portuguese']] = df_aux[['english', 'spanish', 'portuguese']]
    
    df_file.to_csv(PATH_TRANSLATION_CSV, header = True, index=False, sep = '|', encoding=encoding)



# This function is the kernel of the script.
def translation_generator(df, encoding_csv):
    
    batch_elements = 50 # Each API call returns 50 translations
    
    mask = (df['english'].isna()) # Boolean mask with conditions. We get the rows we want them to be translated
    df_filtered = df[~mask]
    mask = ((df['portuguese'].isna()) & (df['spanish'].isna()))
    df_filtered2 = df_filtered[mask]
    
    total_rows = df_filtered2.shape[0] # Total correct rows in translations v5.csv file

    groups = [df_filtered2[i:i+batch_elements] for i in range(0, total_rows, batch_elements)] # Contains "n" batches of "batch_elements" rows. n = number of API calls = number of prompts needed
    # df_with_translations = pd.DataFrame()

    i = 0
    total_rows_translated = 0
    total_execution_time = 0

    for index, group in enumerate(groups):  # For each batch
        print("")
        print("#########################")
        print("### Iteration ", index, " ###")    
        print("#########################\n")

        if (i <= 0):      
            start_time = time.time()
            create_prompt(group, encoding_csv) # Create Prompt
            response = openAI_API_call(encoding_csv) # API call that returns the translations
            save_raw_GPTresponse(response, encoding_csv) # Save response into a GPTresponse.txt file

            df_aux = pd.read_csv(PATH_GPTresponse_TXT, delimiter="|",encoding=encoding_csv, index_col=0) # Read the "GPTresponse" file and convert it into a dataframe "aux". We get the index column  of the response as the index of dataframe
            # df_with_translations = pd.concat([df_with_translations,df_aux], ignore_index=False) # Concat the aux dataframe into the total translations dataframe called "df_with_translations"
            
            save_translations(df_aux, encoding_csv) # Updates translations v5.csv with new translations generated

            i = i + 1
            total_rows_translated += group.shape[0]

            end_time = time.time()
            iteration_time = end_time - start_time
            total_execution_time += iteration_time

            print("")
            print("### Number of rows translated:", total_rows_translated)
            print(f"### Iteration execution time: {iteration_time:.2f} seconds")
            print(f"### Total execution time: {total_execution_time:.2f} seconds")
            
        else:
            i = i + 1
            break
    



############################################################################
################################### MAIN ###################################
############################################################################

PATH_TRANSLATION_CSV = "./translations v5.csv" # File to be translated
PATH_PROMPTFILE_TXT = "./resources/promptTranslations.txt" # File with the future prompt
PATH_GPTresponse_TXT = "./resources/GPTresponse.txt" # File with the future OpenAI API response

# client = OpenAI(api_key="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") # API de carlos
client = OpenAI(api_key="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")
if __name__ == "__main__":

    print("### MAIN ###")

    encoding_csv = detect_encoding(PATH_TRANSLATION_CSV) # Detection of .csv encoding
    # encoding_csv = "utf-8"
    df = ImportCSV(PATH_TRANSLATION_CSV, encoding_csv) # Import PATH_TRANSLATION_CSV file into a Dataframe

    if isinstance (df, pd.DataFrame): # If there is no error
        # analysis_csv(df) # Analysis of CSV dataframe
        translation_generator(df, encoding_csv)
    else:
        print(df)

    print("### END ###")