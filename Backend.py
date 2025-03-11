from flask import Flask, render_template, request
import ipaddress
import math

app = Flask(__name__)

def obtener_clase(ip):
    """Determina la clase de red según la dirección IP ingresada."""
    primer_octeto = int(ip.split('.')[0])
    if 1 <= primer_octeto <= 126:
        return "A", 8
    elif 128 <= primer_octeto <= 191:
        return "B", 16
    elif 192 <= primer_octeto <= 223:
        return "C", 24
    else:
        return None, None

def calcular_mascara(hosts_necesarios):
    """Calcula la máscara de subred mínima para soportar la cantidad de hosts necesarios."""
    n = math.ceil(math.log2(hosts_necesarios + 2))  # +2 para red y broadcast
    nueva_mascara = 32 - n
    return nueva_mascara

def calcular_subredes(ip_base, conexiones):
    """Calcula las subredes en función de la IP base y conexiones necesarias."""
    clase, mascara_base = obtener_clase(ip_base)
    if not clase:
        return []  # IP fuera de rango válido
    
    subred_actual = ipaddress.IPv4Network(f"{ip_base}/{mascara_base}", strict=False)
    resultados = []
    
    for i, hosts_necesarios in enumerate(sorted(conexiones, reverse=True)):
        nueva_mascara = calcular_mascara(hosts_necesarios)
        
        subred = next(subred_actual.subnets(new_prefix=nueva_mascara))
        
        resultados.append({
            "id": f"Red {i+1}",
            "hosts_necesarios": hosts_necesarios,
            "hosts_reales": (2 ** (32 - nueva_mascara)) - 2,
            "mascara": str(subred.netmask),
            "primera_ip": str(subred.network_address + 1),
            "ultima_ip": str(subred.broadcast_address - 1),
            "broadcast": str(subred.broadcast_address)
        })
        
        subred_actual = ipaddress.IPv4Network((int(subred.broadcast_address) + 1, nueva_mascara), strict=False)
    
    return resultados

@app.route("/", methods=["GET", "POST"])
def index():
    subredes = None
    mascara_calculada = None
    
    if request.method == "POST":
        ip_base = request.form.get("ip")
        hosts = request.form.get("hosts")

        if hosts:  # Verifica si el campo hosts fue enviado
            hosts = int(hosts)
            mascara_calculada = calcular_mascara(hosts)

        conexiones = request.form.get("conexiones")
        if conexiones:
            conexiones = [int(x) for x in conexiones.split(",")]
            subredes = calcular_subredes(ip_base, conexiones)

    return render_template("index.html", subredes=subredes, mascara_calculada=mascara_calculada)

if __name__ == "__main__":
    app.run(debug=True)
