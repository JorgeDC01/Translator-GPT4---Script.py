# Translator_GenerativeModel

## Resumen
Este es un script que tiene como objetivo resolver una tarea concreta sobre un archivo "translations v5.csv". Este archivo tiene 3 columnas involucradas en la tarea: [english,portuguese,spanish].
La idea es traducir aquellos literales de la columna "english" en "portuguese" y "spanish". Aquellas filas que ya estén traducidas se mantienen intactas.
Para resolver las traducciones, se realizan llamadas a la API de OpenAI y se necesita una API_KEY con un plan de pago. El modelo generativo elegido por defecto es gpt-4-0613, el cual ofrece una mayor calidad de traducción. 
Cuando se hace una llamada a la API, se utiliza un prompt. En este prompt, se insertan los literales en inglés mencionados anteriormente. 

El proceso simplificado del script es el siguiente:
* Primero, se lee el archivo "csv" con los datos. El path de este archivo se encuentra en la variable PATH_TRANSLATION_CSV.
* En la función "translation_generator", se crean grupos de literales en inglés a traducir. El numero de elementos de cada grupo depende de la variable global "BATCH_ELEMENTS_PARAM" (por defecto, 50).
  Eso significa que cada llamada a la API devuelve la traducción de como mucho 50 filas del "csv". Además, estos grupos no contienen las filas que ya están traducidas.
  El prompt que se enviará por cada grupo a la API se escribe en un archivo "./resources/promptTranslations.txt".
  La respuesta del modelo generativo para cada grupo se escribe en un archivo llamado "./resources/GPTresponse.txt".
  La función de ambos archivos es para testear el script. 
* Por último, se añaden las traducciones al fichero "translations v5.csv".

## Parámetros del script importantes
- El PATH del archivo csv donde se encuentran los datos de entrada se puede modificar en la variable global "PATH_TRANSLATION_CSV".
- El número de traducciones por llamada a la API se puede modificar en la variable global "BATCH_ELEMENTS_PARAM". En el script, por defecto toma el valor 50. No es recomendable poner un valor alto porque el modelo puede no devolver bien la respuesta.
- El número de grupos de 50 literales a traducir se puede modificar en la variable global "N_GROUPS_PROCESSED". El número de grupos de literales definidos a partir del archivo "translations v5.csv" puede ser muy grande si hay muchos datos en él.

## Ejecución del script
Es un requisito indispensable tener python instalado y las librerías necesarias: openai, chardet. 
Para instalarlas:
`pip install openai`
`pip install chardet`

Es un requisito indispensable configurar una variable de entorno llamada "OPENAI_API_KEY" que tenga como contenido tu API KEY.

La ejecución del script se realiza de esta forma: `python .\script_translator.py`

## Ejemplo de ejecución  
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
