import subprocess
import time
import os
from pyngrok import ngrok
from IPython.display import clear_output

def run_start_sh():
    print("Ejecutando start.sh con puerto dinámico...")
    env = os.environ.copy()
    env['GRADIO_SERVER_PORT'] = '0'  # Esto hará que Gradio elija un puerto disponible
    process = subprocess.Popen(['bash', 'start.sh'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               env=env)
    
    # Esperar y buscar el puerto en la salida
    port = None
    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())
        if "Running on local URL:" in line.decode():
            port = int(line.decode().split(":")[-1].strip())
            break
    
    if port is None:
        print("No se pudo determinar el puerto. Error al iniciar el servidor XTTS.")
        stdout, stderr = process.communicate()
        print("Error estándar:", stderr.decode())
        return None, None
    
    print(f"Servidor XTTS iniciado correctamente en el puerto {port}.")
    return process, port

def setup_ngrok(port):
    print(f"Configurando ngrok para el puerto {port}...")
    try:
        public_url = ngrok.connect(port)
        print(f'Accede a la aplicación aquí: {public_url}')
        return public_url
    except Exception as e:
        print(f"Error al configurar ngrok: {str(e)}")
        return None

def main():
    server_process, port = run_start_sh()
    if server_process is None:
        return

    public_url = setup_ngrok(port)
    if public_url is None:
        server_process.terminate()
        return

    print("Servidor XTTS y ngrok configurados correctamente.")
    print("El servidor está en ejecución. Puedes acceder a él a través de la URL de ngrok proporcionada arriba.")
    print("Cuando hayas terminado, ejecuta la función stop_server() para detener el servidor y ngrok.")

def stop_server():
    print("Deteniendo el servidor y ngrok...")
    ngrok.kill()
    # Aquí podrías añadir código adicional para detener el proceso de start.sh si es necesario

# Estas funciones se pueden llamar desde el notebook de Colab
