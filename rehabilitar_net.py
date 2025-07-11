import subprocess

def habilitar_adaptadores_red():
    # Obtener la lista de nombres de adaptadores deshabilitados
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
        if 'Desconectado' in linea or 'Deshabilitado' in linea or 'Disabled' in linea or 'Disconnected' in linea:
            partes = linea.strip().split()
            nombre = " ".join(partes[3:])
            interfaces.append(nombre)

    # Habilitar cada interfaz
    for interfaz in interfaces:
        print(f"Habilitando: {interfaz}")
        subprocess.run(
            ['netsh', 'interface', 'set', 'interface', interfaz, 'admin=enabled'],
            shell=True
        )

if __name__ == '__main__':
    habilitar_adaptadores_red()
