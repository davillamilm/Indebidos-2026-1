import socket
import threading
from gpiozero import LEDBoard
from time import sleep

# --- CONFIGURACIÓN DE LOS LEDS ---
secuencia = LEDBoard(17, 27, 22, 10, 9)
frecuencias = [0.4, 0.3, 0.2, 0.1, 0.05, 0.02]

# Variables de control global
corriendo_cascada = False

def bucle_luces():
    """Esta función se ejecutará en segundo plano de forma infinita"""
    global corriendo_cascada
    while True:
        # Si la señal cambia a falso, detenemos el show de luces inmediatamente
        if not corriendo_cascada:
            secuencia.off()
            sleep(0.1) # Pequeña pausa para no saturar el procesador
            continue

        # Ejecutamos tu secuencia de luces exacta
        for velocidad in frecuencias:
            # Condición de salida rápida: si cambian el comando a mitad de la secuencia
            if not corriendo_cascada:
                break

            if velocidad == 0.02:
                vueltas = 30
            else:
                vueltas = 3

            for _ in range(vueltas):
                if not corriendo_cascada:
                    break
                for led in secuencia:
                    led.on()
                    sleep(velocidad)
                    led.off()

# --- CONFIGURACIÓN E INICIO DEL HILO ---
# Arrancamos el hilo secundario antes de que el Bluetooth se conecte
hilo_luces = threading.Thread(target=bucle_luces, daemon=True)
hilo_luces.start()


# --- CONFIGURACIÓN DEL BLUETOOTH ---
server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server_sock.bind((socket.BDADDR_ANY, 1))
server_sock.listen(1)

print("Esperando conexión desde la app Serial Bluetooth Terminal...")

try:
    client_sock, client_info = server_sock.accept()
    print(f"¡Conectado exitosamente a: {client_info[0]}!")

    while True:
        data = client_sock.recv(1024)
        if not data:
            print("El cliente se ha desconectado.")
            break

        mensaje = data.decode('utf-8').strip().lower()
        print(f"Mensaje recibido: {mensaje}")

        # --- REACCIÓN INMEDIATA A LOS COMANDOS ---
        if mensaje == "avanzar":
            if not corriendo_cascada:
                print("--> [Acción]: Activando ciclo continuo de luces...")
                corriendo_cascada = True
            else:
                print("--> [Aviso]: El ciclo ya está corriendo.")

        elif mensaje == "detener":
            print("--> [Acción]: Frenando ciclo y apagando LEDs de inmediato.")
            corriendo_cascada = False
            secuencia.off() # Forzar el apagado instantáneo

        else:
            print(f"--> Comando no reconocido: {mensaje}")

except KeyboardInterrupt:
    print("\nPrograma finalizado por el usuario.")

finally:
    corriendo_cascada = False
    secuencia.off()
    if 'client_sock' in locals():
        client_sock.close()
    server_sock.close()
    print("Conexiones cerradas correctamente.")
