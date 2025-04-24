document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // 1. Selector de Formatos (Nueva funcionalidad)
    // =============================================
    const formatButtons = document.querySelectorAll('.format-btn');
    
    formatButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remover clase 'active' de todos los botones
            formatButtons.forEach(btn => btn.classList.remove('active'));
            // Añadir clase 'active' al botón clickeado
            this.classList.add('active');
            const selectedFormat = this.dataset.format;
            
            // Actualizar toda la interfaz con el formato seleccionado
            updateDisplayFormat(selectedFormat);
        });
    });

    // Función para cambiar el formato de visualización
    function updateDisplayFormat(format) {
        // 1. Actualizar direcciones en la tabla de subredes
        document.querySelectorAll('[data-ip]').forEach(element => {
            const ipData = JSON.parse(element.dataset.ip);
            element.textContent = ipData[format]?.red || ipData.decimal.red;
        });

        document.querySelectorAll('[data-mask]').forEach(element => {
            const maskData = JSON.parse(element.dataset.mask);
            element.textContent = format === 'decimal' 
                ? `${maskData.decimal.mascara} (/${maskData.decimal.prefixlen})` 
                : maskData[format]?.mascara || maskData.decimal.mascara;
        });

        document.querySelectorAll('[data-first]').forEach(element => {
            const firstData = JSON.parse(element.dataset.first);
            element.textContent = firstData[format]?.primera_ip || firstData.decimal.primera_ip;
        });

        document.querySelectorAll('[data-last]').forEach(element => {
            const lastData = JSON.parse(element.dataset.last);
            element.textContent = lastData[format]?.ultima_ip || lastData.decimal.ultima_ip;
        });

        document.querySelectorAll('[data-broadcast]').forEach(element => {
            const broadcastData = JSON.parse(element.dataset.broadcast);
            element.textContent = broadcastData[format]?.broadcast || broadcastData.decimal.broadcast;
        });

        // 2. Actualizar hosts válidos
        document.querySelectorAll('.host-ip').forEach(element => {
            const originalIP = element.dataset.ip;
            element.textContent = convertIPFormat(originalIP, format);
        });

        // 3. Actualizar direcciones de red y broadcast
        const networkAddr = document.getElementById('network-addr');
        const broadcastAddr = document.getElementById('broadcast-addr');
        
        if (networkAddr && broadcastAddr) {
            networkAddr.textContent = convertIPFormat(networkAddr.textContent, format);
            broadcastAddr.textContent = convertIPFormat(broadcastAddr.textContent, format);
        }
    }

    // Función para convertir una IP a diferentes formatos
    function convertIPFormat(ip, format) {
        if (!ip) return '';
        
        try {
            const octets = ip.split('.');
            
            switch(format) {
                case 'binario':
                    return octets.map(oct => parseInt(oct).toString(2).padStart(8, '0')).join('.');
                case 'hexadecimal':
                    return octets.map(oct => parseInt(oct).toString(16).padStart(2, '0')).join('.');
                default: // decimal
                    return ip;
            }
        } catch (e) {
            console.error("Error al convertir formato:", e);
            return ip;
        }
    }

    // =============================================
    // 2. Validación de Formularios (Existente)
    // =============================================
    // Validación para IPs
    const ipInputs = document.querySelectorAll('input[type="text"][name*="ip"]');
    ipInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9.]/g, '');
        });
    });
    
    // Validación para máscaras
    const maskInputs = document.querySelectorAll('input[name*="mascara"]');
    maskInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9./]/g, '');
        });
    });
    
    // Validación para conexiones
    const conexionesInput = document.getElementById('conexiones');
    if(conexionesInput) {
        conexionesInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9,]/g, '');
        });
    }

    // =============================================
    // 3. Tooltips para Información (Nueva funcionalidad)
    // =============================================
    const infoIcons = document.querySelectorAll('.info-icon');
    infoIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            // Implementar tooltips si es necesario
        });
    });
});