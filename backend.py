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
        return None, None
    except (ValueError, IndexError, AttributeError):
        return None, None

def calcular_mascara(hosts_necesarios):
    """Calcula la máscara de subred mínima para soportar la cantidad de hosts necesarios."""
    try:
        hosts = int(hosts_necesarios)
        if hosts <= 0:
            return None
        n = math.ceil(math.log2(hosts + 2))  # +2 para red y broadcast
        return 32 - n if (32 - n) >= 0 else None
    except (ValueError, TypeError):
        return None

def calcular_subredes(ip_base, conexiones):
    """Calcula las subredes en función de la IP base y conexiones necesarias."""
    try:
        clase, mascara_base = obtener_clase(ip_base)
        if not clase:
            return {"subredes": [], "total_subredes": 0}
        
        # Convertimos conexiones a strings antes de validarlas
        conexiones_validas = [int(str(c).strip()) for c in conexiones if str(c).strip().isdigit()]
        if not conexiones_validas:
            return {"subredes": [], "total_subredes": 0}

        subred_actual = ipaddress.IPv4Network(f"{ip_base}/{mascara_base}", strict=False)
        resultados = []
        
        for i, hosts_necesarios in enumerate(sorted(conexiones_validas, reverse=True), 1):
            nueva_mascara = calcular_mascara(hosts_necesarios)
            if not nueva_mascara:
                continue
                
            try:
                subred = next(subred_actual.subnets(new_prefix=nueva_mascara))
                resultados.append({
                    "id": f"Red {i}",
                    "direccion_subred": str(subred.network_address),
                    "hosts_necesarios": hosts_necesarios,
                    "hosts_reales": (2 ** (32 - nueva_mascara)) - 2,
                    "mascara": str(subred.netmask),
                    "prefixlen": nueva_mascara,
                    "primera_ip": str(subred.network_address + 1),
                    "ultima_ip": str(subred.broadcast_address - 1),
                    "broadcast": str(subred.broadcast_address)
                })
                subred_actual = ipaddress.IPv4Network((int(subred.broadcast_address) + 1, nueva_mascara), strict=False)
            except ValueError as e:
                print(f"Error creando subred {i}: {e}")
                continue
        
        return {
            "subredes": resultados,
            "total_subredes": len(resultados)
        }
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
        print(f"Error al calcular subredes: {e}")
        return {"subredes": [], "total_subredes": 0}
        
def calcular_host(ip_base, mascara):
    from ipaddress import ip_network

    # Crear red a partir de IP base y máscara
    red = ip_network(f"{ip_base}/{mascara}", strict=False)

    # Hosts disponibles (total - 2 por red y broadcast)
    hosts_disponibles = red.num_addresses - 2

    return {
        "direccion_red": str(red.network_address),
        "direccion_broadcast": str(red.broadcast_address),
        "hosts_disponibles": hosts_disponibles,
        "hosts_validos": [str(ip) for ip in red.hosts()]
    }


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

@app.route("/", methods=["GET", "POST"])
def index():
    data = {
        "subredes": None,
        "total_subredes": None,
        "mascara_calculada": None,
        "netmask": None,
        "hosts_info": None,
        "error": None
    }

    if request.method == "POST":
        try:
            ip_base = request.form.get("ip", "").strip()
            conexiones = request.form.get("conexiones", "").strip()
            mascara = request.form.get("mascara", "").strip()
            hosts = request.form.get("hosts", "").strip()

            # Validación de IP
            try:
                if ip_base:
                    ipaddress.IPv4Address(ip_base)
            except ValueError:
                data["error"] = "Dirección IP no válida"
            else:
                # Cálculo por hosts necesarios
                if hosts and hosts.isdigit():
                    hosts_requeridos = int(hosts)
                    data["mascara_calculada"] = calcular_mascara(hosts_requeridos)
                    
                    if data["mascara_calculada"]:
                        netmask_calculada = ipaddress.IPv4Network(f'0.0.0.0/{data["mascara_calculada"]}').netmask
                        data["netmask"] = str(netmask_calculada)
                    else:
                        data["error"] = "Número de hosts demasiado grande para una subred válida"


                # Cálculo por conexiones
                if conexiones:
                    conexiones_lista = [c.strip() for c in conexiones.split(",") if c.strip().isdigit()]
                    if conexiones_lista:
                        resultado = calcular_subredes(ip_base, conexiones_lista)
                        data["subredes"] = resultado["subredes"]
                        data["total_subredes"] = resultado["total_subredes"]

                # Cálculo por IP/Máscara
                if mascara:
                    try:
                        red = ipaddress.IPv4Network(f"{ip_base}/{mascara}", strict=False)
                        data["subredes"] = calcular_subredes_conIPMascara(ip_base, mascara)
                        data["hosts_info"] = calcular_host(ip_base, mascara)
                    except ValueError:
                        data["error"] = "Formato de máscara no válido"


        except Exception as e:
            data["error"] = f"Error en el procesamiento: {str(e)}"
            print(data["error"])

    return render_template("index.html", **data)
