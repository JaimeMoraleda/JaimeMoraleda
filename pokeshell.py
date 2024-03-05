import os
import subprocess
import sys
import signal
import requests

# Variables globales para almacenar la selección del Pokémon inicial y los PIDs
pokemon_seleccionado = None
padre_pid = None

def obtener_ubicacion_script():
    return os.path.dirname(os.path.realpath(__file__))

def obtener_pid_launcher():
    global padre_pid
    padre_pid = os.getppid()
    print(f"PID del launcher: {padre_pid}")

def inicializador_pokemon():
    global pokemon_seleccionado
    print("="*100)
    print("\033[1;37m" + "Bienvenido al PokeShell (BETA), ingrese el starter a iniciar" + "\033[0m")
    print("\033[1;37m" + " " * 25 + "1) Charmander" + "\033[0m")
    print("\033[1;37m" + " " * 25 + "2) Bulbasaur" + "\033[0m")
    print("\033[1;37m" + " " * 25 + "3) Squirtle" + "\033[0m")
    print("="*100)
    pokemon = input("Ingrese su inicial: ").lower()

    # Verificación del Pokémon inicial
    while True:
        if pokemon == "charmander":
            print("\033[1;31m" + "Has escogido a Charmander" + "\033[0m")
            pokemon_seleccionado = pokemon
            return pokemon
        elif pokemon == "bulbasaur":
            print("\033[1;32m" + "Has escogido a Bulbasaur" + "\033[0m")
            pokemon_seleccionado = pokemon
            return pokemon
        elif pokemon == "squirtle":
            print("\033[1;34m" + "Has escogido a Squirtle" + "\033[0m")
            pokemon_seleccionado = pokemon
            return pokemon
        else:
            pokemon = input("\033[1;37m" + f'El Pokémon {pokemon} no está dentro de los iniciales a escoger.\n'
                            f'\n'
                            f'{"="*100}\n'
                            f'Bienvenido al PokeShell (BETA), ingrese el starter a iniciar\n'
                            f'{" "*25}1) Charmander\n'
                            f'{" "*25}2) Bulbasaur\n'
                            f'{" "*25}3) Squirtle\n'
                            f'{"="*100}\n'
                            f'Ingrese de nuevo el inicial a escoger: ' + "\033[0m").lower()

def obtener_informacion_pokemon(nombre_pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}/'
    respuesta = requests.get(url)

    while respuesta.status_code != 200:
        print(f"No se pudo obtener información para {nombre_pokemon.capitalize()}")
        nombre_pokemon = input("Ingrese el nombre del Pokémon nuevamente: ")
        url = f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}/'
        respuesta = requests.get(url)

    datos_pokemon = respuesta.json()
    print(f"Información de {nombre_pokemon.capitalize()}:")
    print(f"Nombre: {datos_pokemon['name'].capitalize()}")
    print(f"ID: {datos_pokemon['id']}")
    print("Tipos:", ', '.join([tipo['type']['name'].capitalize() for tipo in datos_pokemon['types']]))
    print(f"Altura: {datos_pokemon['height'] / 10} metros")
    print(f"Peso: {datos_pokemon['weight'] / 10} kilogramos")

def mostrar_ascii_art(pokemon):
    if pokemon == "charmander":
        color_pokemon = "\033[1;31m"  # Rojo para Charmander
        ascii_art = """
              _.--\"\"`-..\n
            ,'          `.\n
          ,'          __  `.\n
         /|          \" __   \\\n
        , |           / |.   .\n
        |,'          !_.'|   |\n
      ,'             '   |   |\n
     /              |`--'|   |\n
    |                `---'   |\n
     .   ,                   |                       ,\".\n
      ._     '           _'  |                    , ' \\ `\n
  `.. `.`-...___,...---\"\"    |       __,.        ,`\"   L,|\n
  |, `- .`._        _,-,.'   .  __.-'-. /        .   ,    \\\n
  -:..     `. `-..--_.,.<       `\"      / `.        `-/ |   .\n
  `,         \"\"\"\"'     `.              ,'         |   |  ',,\n
    `.      '            '            /          '    |'. |\n
      `.   |              \\       _,-'           |       ''\n
        `._'               \\   '\"\\                .      |\n
           |                '     \\                `._  ,'\n
           |                 '     \\                 .'|\n
           |                 .      \\                | |\n
           |                 |       L              ,' |\n
           `                 |       |             /   '\n
            \\                |       |           ,'   /\n
          ,' \\               |  _.._ ,-..___,..-'    ,'\n
         /     .             .      `!             ,j'\n
        /       `.          /        .           .'/\n
       .          `.       /         |        _.'.'\n
        `.          7`'---'          |------\"'_.'\n
       _,.`,_     _'                ,''-----\"'\n
   _,-_    '       `.     .'      ,\\n
   -\" /`.         _,'     | _  _  _.|\n
    \"\"--'---\"\"\"\"\"'        `' '! |! /\n
                            `\" \" -' mh\n"""
    elif pokemon == "bulbasaur":
        color_pokemon = "\033[1;32m"  # Verde para Bulbasaur
        ascii_art = """
                                            /\\n
                         _,.------....___,.' ',.-.\\n
                      ,-'          _,.--\"        |\\n
                    ,'         _.-'              .\\n
                   /   ,     ,'                   `\\n
                  .   /     /                     ``.\\n
                  |  |     .                       \\.\\\\n
        ____      |___._.  |       __               \\ `.\\n
      .'    `---\"\"       ``\"-.--\"'`  \\               .  \\\\n
     .  ,            __               `              |   .\\n
     `,'         ,-\"'  .               \\             |    L\\n
    ,'          '    _.'                -._          /    |\\n
   ,`-.    ,\".   `--'                      >.      ,'     |\\n
  . .'\\'   `-'       __    ,  ,-.         /  `.__.-      ,'\n
  ||:, .           ,'  ;  /  / \\ `        `.    .      .'/\n
  j|:D  \\          `--'  ' ,'_  . .         `.__, \\   , /\n
 / L:_  |                 .  \"' :_;                `.'.'\n
 .    \"\"'                  \"\"\"\"\"'                    V\n
  `.                                 .    `.   _,..  `\\n
    `,_   .    .                _,-'/    .. `,'   __  `\\n
     ) \\\\`._        ___....----\"'  ,'   .'  \\\\ |   '  \\\\  .\n
    /   `. \"`-.--\"'         _,.' ,'     `---' |    `./  |\n
   .   _  `\"\"'--.._____..--\"   ,             '         |\n
   | .\" `. `-.                /-.           /          ,\n
   | `._.'    `,_            ;  /         ,'          .\n
  .'          /| `-.        . ,'         ,           ,\n
   `---.__,--.','    '`-..___;-...__   ,.'\\\\ ____.___.'\n
  `\"^--'..'   '-`-^-'\"--    `-^-'`.''\"\"\"\"\"`.,^.`.--' mh\n
 \\n
 \\n
"""
    elif pokemon == "squirtle":
        color_pokemon = "\033[1;34m"  # Azul para Squirtle
        ascii_art = """
               _,........__\\n
            ,-'            \"`-.\\n
          ,'                   `-.\\n
        ,'                        \\\\n
      ,'                           .\\n
      .'\\               ,\"\".       `\\n
     ._.'|             / |  `       \\\\n
     |   |            `-.'  ||       `.\\n
     |   |            '-._,'||       | \\\\n
     .`.,'             `..,'.'       , |`-.\\n
     l                       .'`.  _/  |   `\\.\\n
     `-.._'-   ,          _ _'   -\" \\\\  .     `\\n
`.\"\"\"\"\"'-.`-...,---------','         `. `....__.\\n
.'        `\"-..___      __,'\\\\          \\\\  \\\\     \\\\n
\\_ .          |   `\"\"\"\"'    `.           . \\\\     \\\\n
  `.          |              `.          |  .     L\\n
    `.        |`--...________.'.        j   |     |\\n
      `._    .'      |          `.     .|   ,     |\\n
         `--,\\\\       .            `7\"\"' |  ,      |\\n
            ` `      `            /     |  |      |    _,-'\"\"\"`-.\n
             \\\\ `.     .          /      |  '      |  ,'          `.\n
              \\\\  v.__  .        '       .   \\\\    /| /              \\\\\n
               \\/    `\"\"\\\\\"\"\"\"\"\"\"`.       \\\\   \\\\  /.''                |\n
                `        .        `._ ___,j.  `\\\\ / .-       ,---.     |\n
                ,`-.      \\\\         .\"     \\\\. |/        j     `    |\n
               /    \\\\`.     \\\\       /         \\\\ /         |     /    j\n
              |       `-.   7-.._ .          |\"          '         /\n
              |          `./_    `|          |            .     _,'\n
              `.           / `----|          |-............`---'\n
                \\\\          \\\\      |          |\n
               ,'           )     \\\\         |\n
                7____,,..--'      /          |\n
                                  `---.__,--.'mh\n
"""
    else:
        color_pokemon = ""  # No se especifica color para otros Pokémon
        ascii_art = ""

    return color_pokemon, ascii_art

def mostrar_comandos_disponibles():
    print("Comandos disponibles:")
    print("- ch.starter: Cambiar el Pokémon inicial.")
    print("- exit: Salir del programa.")
    print("- info.pokemon [nombre]: Obtener información sobre un Pokémon.")
    print("- sh.inicial: Mostrar el ASCII art del Pokémon inicial.")
    print("- pid.info: Mostrar PID del programa y del launcher.")
    print("- kill-9 [PID]: Eliminar un proceso con su PID.")
    print("- help.pokemon: Mostrar esta lista de comandos.")

def mostrar_pokemon_seleccionado():
    global pokemon_seleccionado
    if pokemon_seleccionado:
        color_pokemon, ascii_art = mostrar_ascii_art(pokemon_seleccionado)
        print(color_pokemon + ascii_art + "\033[0m")
    else:
        print("No se ha seleccionado ningún Pokémon inicial.")

def obtener_pid_programa():
    print(f"PID del programa: {os.getpid()}")

def obtener_pid_padre():
    obtener_pid_launcher()
    obtener_pid_programa()

def matar_proceso(pid):
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"Proceso con PID {pid} eliminado correctamente.")
    except OSError:
        print(f"No se pudo eliminar el proceso con PID {pid}.")

def main():
    global pokemon_seleccionado
    ubicacion_script = obtener_ubicacion_script()
    logo_impreso = False
    
    while True:
        if not logo_impreso:
            print("\033[1;37m" + """
   ____            _             ____    _              _   _ 
  |  _ \    ___   | | __   ___  / ___|  | |__     ___  | | | |
  | |_) |  / _ \  | |/ /  / _ \ \___ \  | '_ \   / _ \ | | | |
  |  __/  | (_) | |   <  |  __/  ___) | | | | | |  __/ | | | |
  |_|      \___/  |_|\_\  \___| |____/  |_| |_|  \___| |_| |_|
                                                             
""" + "\033[0m")
            logo_impreso = True
        
        if pokemon_seleccionado is None:
            inicializador_pokemon()
        
        while pokemon_seleccionado:
            # Obtener el color según el Pokémon seleccionado
            color_prompt, _ = mostrar_ascii_art(pokemon_seleccionado)
            
            # Obtener la ubicación actual del directorio
            ubicacion_actual = os.getcwd()

            # Imprimir la ubicación actual y el prompt con el color correspondiente
            print(color_prompt + f"{ubicacion_actual}> " + "\033[0m", end="")
            
            comando = input()
            if comando.lower() == 'exit':
                sys.exit()  # Terminar completamente el programa si se ingresa 'exit'
            elif comando.lower().startswith('cd'):
                partes = comando.split(maxsplit=1)
                if len(partes) == 1:  # No se especifica ningún directorio
                    os.chdir(os.path.expanduser('~'))  # Cambiar al directorio de inicio del usuario
                else:
                    nuevo_directorio = partes[1].strip()
                    try:
                        os.chdir(nuevo_directorio)  # Cambiar al directorio especificado
                    except FileNotFoundError:
                        print("El directorio especificado no existe.")
            elif comando.lower().startswith('nano'):
                partes = comando.split(maxsplit=1)
                if len(partes) == 1:  # No se especifica ningún archivo
                    print("Por favor, especifique el archivo a editar con nano.")
                else:
                    archivo = partes[1].strip()
                    subprocess.run(['nano', archivo])
            elif comando.lower().startswith('info.pokemon'):
                if pokemon_seleccionado:
                    nombre_pokemon = comando.split(maxsplit=1)[1].strip()
                    obtener_informacion_pokemon(nombre_pokemon)
                else:
                    print("No se ha seleccionado ningún Pokémon para buscar información.")
            elif comando.lower() == 'ch.starter':
                pokemon_seleccionado = None
                break
            elif comando.lower() == 'sh.inicial':
                mostrar_pokemon_seleccionado()
            elif comando.lower() == 'sh.evo':
                print("Funcionalidad de mostrar la evolución no implementada.")
            elif comando.lower() == 'help.pokemon':
                mostrar_comandos_disponibles()
            elif comando.lower() == 'pid.info':
                obtener_pid_padre()
            elif comando.lower().startswith('kill-9'):
                partes = comando.split(maxsplit=1)
                if len(partes) == 1:  # No se especifica ninguna PID
                    print("Por favor, especifique la PID del proceso a eliminar.")
                else:
                    pid = int(partes[1].strip())
                    matar_proceso(pid)
            else:
                partes = comando.split()
                cmd = partes[0]
                args = partes[1:]

                try:
                    # Verificar si el comando es un archivo Bash
                    if cmd.endswith('.sh'):
                        subprocess.run(['bash', cmd] + args)
                    else:
                        proceso = subprocess.Popen([cmd] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        salida, error = proceso.communicate()

                        if salida:
                            print(salida.decode("utf-8"))
                        if error:
                            print(error.decode("utf-8"), file=sys.stderr)
                except PermissionError:
                    print("Permiso denegado para ejecutar el comando.")
                except FileNotFoundError:
                    print("El comando especificado no se encontró.")

if __name__ == "__main__":
    main()
