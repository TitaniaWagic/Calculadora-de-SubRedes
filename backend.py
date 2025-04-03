from flask import Flask, render_template, request
import ipaddress
import math

app = Flask(__name__)

def obtener_clase(ip):
    """Determina la clase de red según la dirección IP ingresada."""
    try:
        primer_octeto = int(ip.split('.')[0])
        if 1 <= primer_octeto <= 126:
            return "A", 8
        elif 128 <= primer_octeto <= 191:
            return "B", 16
        elif 192 <= primer_octeto <= 223:
            return "C", 24
        else:
            return None, None
    except (ValueError, IndexError, AttributeError):
        return None, None

def calcular_mascara(hosts_necesarios):
    """Calcula la máscara de subred mínima para soportar la cantidad de hosts necesarios."""
    try:
        n = math.ceil(math.log2(int(hosts_necesarios) + 2))  # +2 para red y broadcast
        return 32 - n
    except (ValueError, TypeError):
        return None

def calcular_subredes(ip_base, conexiones):
    """Calcula las subredes en función de la IP base y conexiones necesarias."""
    try:
        clase, mascara_base = obtener_clase(ip_base)
        if not clase:
            return []
        
        subred_actual = ipaddress.IPv4Network(f"{ip_base}/{mascara_base}", strict=False)
        resultados = []
        total_subredes = len(conexiones)  # Calculamos el total de subredes
        
        for i, hosts_necesarios in enumerate(sorted(map(int, conexiones), reverse=True)):
            nueva_mascara = calcular_mascara(hosts_necesarios)
            if not nueva_mascara:
                continue
                
            subred = next(subred_actual.subnets(new_prefix=nueva_mascara))
            
            resultados.append({
                "id": f"Red {i+1}",
                "direccion_subred": str(subred.network_address),  # Nueva línea
                "hosts_necesarios": hosts_necesarios,
                "hosts_reales": (2 ** (32 - nueva_mascara)) - 2,
                "mascara": str(subred.netmask),
                "prefixlen": nueva_mascara,
                "primera_ip": str(subred.network_address + 1),
                "ultima_ip": str(subred.broadcast_address - 1),
                "broadcast": str(subred.broadcast_address)
            })
            
            subred_actual = ipaddress.IPv4Network((int(subred.broadcast_address) + 1, nueva_mascara), strict=False)
        
        # Devolvemos tanto los resultados como el total de subredes
        return {
            "subredes": resultados,
            "total_subredes": total_subredes
        }
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
        print(f"Error al calcular subredes: {e}")
        return {"subredes": [], "total_subredes": 0}

def calcular_subredes_conIPMascara(ip_base, mascara):
    """Calcula las subredes en función de la IP base y la máscara proporcionada."""
    try:
        red = ipaddress.IPv4Network(f"{ip_base}/{mascara}", strict=False)
        resultados = []
        prefixlen = red.prefixlen

        for i in range(2 ** (32 - prefixlen)):
            subred = next(red.subnets(new_prefix=prefixlen))
            
            resultados.append({
                "id": f"Subred {i+1}",
                "mascara": str(subred.netmask),
                "prefixlen": prefixlen,
                "primera_ip": str(subred.network_address + 1),
                "ultima_ip": str(subred.broadcast_address - 1),
                "broadcast": str(subred.broadcast_address),
                "hosts_reales": (2 ** (32 - prefixlen)) - 2
            })
            
            red = ipaddress.IPv4Network((int(subred.broadcast_address) + 1, prefixlen), strict=False)

        return resultados
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
        print(f"Error al calcular subredes con IP/Máscara: {e}")
        return []

def calcular_host(ip_base, mascara):
    """Calcula los hosts válidos en una subred dada la IP base y la máscara."""
    try:
        red = ipaddress.IPv4Network(f"{ip_base}/{mascara}", strict=False)
        return {
            "direccion_red": str(red.network_address),
            "direccion_broadcast": str(red.broadcast_address),
            "hosts_validos": [str(host) for host in red.hosts()],
            "total_hosts": len(list(red.hosts()))
        }
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
        print(f"Error al calcular hosts: {e}")
        return {}

@app.route("/", methods=["GET", "POST"])
def index():
    subredes = None
    mascara_calculada = None
    hosts_info = None
    netmask = None
    error = None

    if request.method == "POST":
        try:
            ip_base = request.form.get("ip", "").strip()
            conexiones = request.form.get("conexiones", "").strip()
            mascara = request.form.get("mascara", "").strip()
            hosts = request.form.get("hosts", "").strip()

            # Validación básica de IP
            if ip_base and not all(0 <= int(octeto) <= 255 for octeto in ip_base.split('.') if octeto.isdigit()):
                error = "Dirección IP no válida"
            else:
                if hosts and hosts.isdigit():
                    mascara_calculada = calcular_mascara(hosts)
                    if mascara_calculada:
                        netmask = str(ipaddress.IPv4Network(f'0.0.0.0/{mascara_calculada}').netmask)

                if conexiones:
                    conexiones_lista = [c.strip() for c in conexiones.split(",") if c.strip().isdigit()]
                    if conexiones_lista:
                        subredes = calcular_subredes(ip_base, conexiones_lista)

                if mascara:
                    if '/' in mascara or all(0 <= int(octeto) <= 255 for octeto in mascara.split('.') if octeto.isdigit()):
                        subredes = calcular_subredes_conIPMascara(ip_base, mascara)
                        hosts_info = calcular_host(ip_base, mascara)
                    else:
                        error = "Formato de máscara no válido"

        except Exception as e:
            error = f"Error en el procesamiento: {str(e)}"
            print(error)

    return render_template(
        "index.html",
        subredes=subredes,
        mascara_calculada=mascara_calculada,
        netmask=netmask,
        hosts_info=hosts_info,
        error=error
    )
