import os
import subprocess
import sys

def install_requirements():
    print("Instalando requerimientos...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
def update_numpy():
    print("Actualizando NumPy...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "numpy"])

def modify_start_sh():
    print("Modificando start.sh...")
    with open('start.sh', 'r') as file:
        content = file.read()
    
    # Eliminar la activación del entorno virtual
    content = content.replace('. venv/bin/activate', '')
    
    # Asegurar que se use un puerto dinámico
    content = content.replace('python xtts_demo.py', 'python xtts_demo.py --server_port=0')
    
    with open('start.sh', 'w') as file:
        file.write(content)

def run_start_sh():
    print("Ejecutando start.sh...")
    process = subprocess.Popen(['bash', 'start.sh'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    # Buscar el puerto en la salida
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
        return None
    
    print(f"Servidor XTTS iniciado correctamente en el puerto {port}.")
    return port

def setup_ngrok(port):
    from pyngrok import ngrok
    print(f"Configurando ngrok para el puerto {port}...")
    try:
        public_url = ngrok.connect(port)
        print(f'Accede a la aplicación aquí: {public_url}')
    except Exception as e:
        print(f"Error al configurar ngrok: {str(e)}")

def main():
    install_requirements()
    update_numpy()
    modify_start_sh()
    port = run_start_sh()
    if port:
        setup_ngrok(port)

if __name__ == "__main__":
    main()
