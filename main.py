import os
import openai
import time
# pip install psutil
# pip install --upgrade openai
import sys
# Configura tu clave de API de OpenAI
openai.api_key = "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"


############################################################################
#################### FUNCIONES CODIGO INPUT Y OUTPUT #######################
############################################################################

# Función para recopilar el codigo del prompt
def leer_codigo_desde_archivos(archivo_input_index, archivo_input_viewmodel):
    codigo_index_viewModel = []
    try:
        with open(archivo_input_index, "r") as file:
            codigo_index = file.read()
            codigo_index_viewModel.append(codigo_index)
            file.close()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo_input_index}'")

    try:
        with open(archivo_input_viewmodel, "r") as file:
            codigo_viewmodel = file.read()
            codigo_index_viewModel.append(codigo_viewmodel)
            file.close()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo_input_viewmodel}'")

    return codigo_index_viewModel


# Función para interactuar con GPT-3
def obtener_respuesta_gpt3(promptFile):
    
    try:
        print("\t ### Iniciando petición a la API ###")

        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            temperature=0.00000001,
            messages=[
                {"role": "user", "content": promptFile},
            ]
        )

        if response and response.choices:
            return response.choices[0].message['content']
        else:
            print("\t ### La respuesta de la API está vacía.")
            return 1
    except openai.error.OpenAIError as e:
        print(f"Error al comunicarse con la API de OpenAI: {e}")
        return 1
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 1

    finally:
        print("\t ### Petición a la API completada ###")


# Función para escribir el código devuelto en la aplicación de React
def escribir_codigo_en_aplicacion_react(codigo_devuelto):
    print("\t ### Iniciando escritura en la APP de React ###")

    # Busca y elimina "```jsx" al principio
    # codigo_devuelto = codigo_devuelto.replace("```jsx", "", 1)
    
    # Busca y elimina "```" al final
    # codigo_devuelto = codigo_devuelto.rsplit("```", 1)[0]

    file = open("./recursos_script/respuestaGPT.txt", "r")
    lines = file.readlines()
    for line in lines:
        if "import" in line and line.find("import") == 0:
            # print("Find")
            start = lines.index(line)
            break
    
    for line in lines:
        if "export default Tabla;" in line:
            end = lines.index(line)
            break
    # print("Linea de import:", start, "; linea de fin:", end)
    lines = lines[start:end+1]
    file.close()
    
    file = open("./app_test_react/src/Tabla.js", "wt")
    for line in lines:
        file.write(f"{line}")
    file.close()


# Escribe el codigo de los test unitarios generados por la API OpenAI GPT en la app de OJET
def escribir_codigo_test_en_aplicacion_OJET(codigo_devuelto):
    print("\t ### Iniciando escritura en la APP de OJET ###")

    start = None
    end = None
    file = open("./recursos_script/respuestaGPT.txt", "r")
    lines_response = file.readlines()

    for line in lines_response:
        if "```javascript" in line:
            # print("Find")
            start = lines_response.index(line)
            break
    
    for index, line in enumerate(lines_response):
        if "```" in line and index != start:
            end = index
            break    

    
    if(start != None and end != None):
        lines = lines_response[start+1:end]
        # Escribir el código extraído en el archivo de salida
        with open("./app_test/test/appControllerSpec.js", "w") as archivo:
            archivo.writelines(lines)
    else:
        # Escribir el código extraído en el archivo de salida
        with open("./app_test/test/appControllerSpec.js", "w") as archivo:
            archivo.writelines(lines_response)        


# Escribe el codigo de los test unitarios generados por la API OpenAI GPT en la app de REACT
def escribir_codigo_test_en_aplicacion_REACT():
    print("\t ### Iniciando escritura en la APP de REACT ###")


# Función que escribe en el fichero ./recursos_script/respuestaGPT.txt para comprobar lo que devuelve la API de OpenAI
def comprobacion_respuesta (respuestaGPT):
    print("\t ### Iniciando escritura de la respuesta en bruto en './recursos_script/respuestaGPT.txt' ###")
    with open("./recursos_script/respuestaGPT.txt", "w") as file:
        file.write(respuestaGPT)
        file.close()
    

#################################################################################################################
# Función que recoge la lógica de generación de código en React a partir de código en OJET.
# Primero, se lee el archivo /prompt.txt que contiene el prompt que se le va a mandar a la API de OpenAI 
# Segundo, se obtiene una respuesta de GPT por medio de la API de OpenAI mediante la función 'obtener_respuesta_gpt3'
# Tercero, se escribe en un archivo respuestaGPT.txt el contenido en bruto de la respuesta mediante la función 'comprobacion_respuesta'
# Cuarto, mediante la función 'escribir_codigo_en_aplicacion_react' se filtra la 'basura' de la respuesta devuelta y se escribe el código generado por GPT en la aplicación de React.
#################################################################################################################

def generar_codigo_OJET_REACT():
    # Proceso de generación de código            
    # Lectura
    # codigos = leer_codigo_desde_archivos(archivo_input_index, archivo_input_viewmodel)

    with open("./recursos_script/prompt_OJET_REACT.txt", "r") as file:
        print("\t ### Iniciando lectura del prompt ###")
        prompt = file.read()
        file.close()

    respuestaGPT = obtener_respuesta_gpt3(prompt)
    if(respuestaGPT != 1): # Si no hay error en la llamada a la API
        comprobacion_respuesta(respuestaGPT)
        escribir_codigo_en_aplicacion_react(respuestaGPT)
    print("")

#################################################################################################################
# Función que genera PRUEBAS UNITARIAS de appController.js de la aplicación Oracle Jet con Karma y Jasmine
#################################################################################################################

def generar_pruebas_OJET():

    with open("./recursos_script/prompt_test_OJET.txt", "r") as file:
        print("\t ### Iniciando lectura del prompt de Prueba OJET ###")
        prompt = file.read()
        file.close()

    respuestaGPT = obtener_respuesta_gpt3(prompt)
    if(respuestaGPT != 1): # Si no hay error en la llamada a la API
        comprobacion_respuesta(respuestaGPT)
        # Escritura test en aplicación OJET
        escribir_codigo_test_en_aplicacion_OJET(respuestaGPT)
    print("")

#################################################################################################################
# Función que genera PRUEBAS UNITARIAS del componente Tabla.js de la aplicación React con JEST
#################################################################################################################

def generar_pruebas_React():

    with open("./recursos_script/prompt_test_REACT.txt", "r") as file:
        print("\t ### Iniciando lectura del prompt de Prueba REACT ###")
        prompt = file.read()
        file.close()

    respuestaGPT = obtener_respuesta_gpt3(prompt)
    if(respuestaGPT != 1): # Si no hay error en la llamada a la API
        comprobacion_respuesta(respuestaGPT)
        # Escritura test en aplicación REACT
        # escribir_codigo_test_en_aplicacion_REACT(respuestaGPT)
    print("")

############################################################################
################################### MAIN ###################################
############################################################################


if __name__ == "__main__":

    print("### MAIN ###")

    # archivo_input_index = "./app_test/src/index.html"
    # archivo_input_viewmodel = "./app_test/src/js/appController.js"

    

    
    print("###############################################################")
    print("############################ MENU #############################")
    print("###############################################################\n")

    
        
    print("### 1. Generacion código en React por medio de '/prompt' con GPT ###")
    print("### 2. Generación de Pruebas con Jasmine de Oracle Jet por medio de '/prompt_test_OJET' con GPT ###")
    print("### 3. Generación de Pruebas con JEST de React por medio de '/prompt_test_REACT' con GPT ###")
    
    if len(sys.argv) > 1:
        modo_oper = sys.argv[1]    

        print("")
        
        match modo_oper.lower():

            case '1':

                print("### Se ha elegido el modo de generación de código en React a partir de código en OJET ###\n")
                generar_codigo_OJET_REACT()
                print("")

            case '2':

                print("### Se ha elegido el modo de generación de Pruebas unitarias en OJET con Jasmine ###\n")
                generar_pruebas_OJET()
                print("")

            case '3':

                print("### Se ha elegido el modo de generación de Pruebas unitarias en React con JEST ###\n")
                generar_pruebas_React()
                print("")

            case 'salir':

                print("### Fin del script... ###\n")

    print("### FINAL PROGRAMA ###")