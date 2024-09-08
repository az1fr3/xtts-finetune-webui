import subprocess
import time
from pyngrok import ngrok
from IPython.display import clear_output

def run_xtts_server():
    # Iniciar el servidor XTTS en segundo plano
    server_process = subprocess.Popen(['bash', 'start.sh'], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
    
    # Esperar un poco para que el servidor inicie
    time.sleep(10)
    
    # Verificar si el proceso sigue en ejecución
    if server_process.poll() is None:
        print("Servidor XTTS iniciado correctamente.")
    else:
        print("Error al iniciar el servidor XTTS.")
        stdout, stderr = server_process.communicate()
        print("Salida estándar:", stdout.decode())
        print("Error estándar:", stderr.decode())
        return

    # Configurar y iniciar ngrok
    try:
        public_url = ngrok.connect(5003)
        print(f'Accede a la aplicación aquí: {public_url}')
    except Exception as e:
        print(f"Error al configurar ngrok: {str(e)}")
        server_process.terminate()
        return

    print("Presiona Ctrl+C para detener el servidor.")
    try:
        # Mantener el script en ejecución
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo el servidor...")
        server_process.terminate()
        ngrok.disconnect(public_url)

# Ejecutar la función principal
if __name__ == "__main__":
    run_xtts_server()
