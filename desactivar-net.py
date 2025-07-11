import subprocess
def desactivar_data_automatica():
    print("⏱️ Desactivant sincronització automàtica de l'hora...")

    # 1. Modifica el registre per impedir la sincronització (Type=NoSync)
    subprocess.run(
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters" /v Type /t REG_SZ /d NoSync /f',
        shell=True
    )

    # 2. Atura el servei de sincronització d’hora
    subprocess.run('sc stop w32time', shell=True)

    # 3. Desactiva l'inici automàtic del servei
    subprocess.run('sc config w32time start= disabled', shell=True)

    print("✅ Sincronització automàtica de l’hora desactivada.")
    
def deshabilitar_adaptadores_red():
    # Obtener la lista de nombres de adaptadores habilitados
    resultado = subprocess.run(
        ['netsh', 'interface', 'show', 'interface'],
        capture_output=True,
        text=True,
        shell=True
    )

    if resultado.returncode != 0:
        print("Error al obtener la lista de interfaces.")
        print(resultado.stderr)
        return

    interfaces = []
    for linea in resultado.stdout.splitlines():
        if 'Conectado' in linea or 'Habilitado' in linea or 'Enabled' in linea or 'Connected' in linea:
            partes = linea.strip().split()
            # El nombre del adaptador está al final
            nombre = " ".join(partes[3:])
            interfaces.append(nombre)

    # Deshabilitar cada interfaz
    for interfaz in interfaces:
        print(f"Deshabilitando: {interfaz}")
        subprocess.run(
            ['netsh', 'interface', 'set', 'interface', interfaz, 'admin=disabled'],
            shell=True
        )
    desactivar_data_automatica()    
    #Format: día-mes-año
    # Demanar la data a l'usuari
    entrada = input("Introdueix la nova data (format DD-MM-YYYY): ")

    try:
        # Separar i reorganitzar al format que Windows espera: MM-DD-YYYY
        dia, mes, any = entrada.split('-')
        nova_data = f"{dia}-{mes}-{any}"

        # Intentar canviar la data
        subprocess.run(f'date {nova_data}', shell=True, check=True)
        print(f"✔ Fecha del sistema cambiada a {entrada}.")
    except ValueError:
        print("❌ Format incorrecte. Assegura't que sigui DD-MM-YYYY.")
    except subprocess.CalledProcessError:
        print("❌ Error al canviar la data. Estàs executant el script com a administrador?")

if __name__ == '__main__':
    deshabilitar_adaptadores_red()
