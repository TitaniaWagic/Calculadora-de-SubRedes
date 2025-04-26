document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // 1. Selector de Formatos (Modificado para nueva estructura)
    // =============================================
    const formatButtons = document.querySelectorAll('.format-btn');
    
    formatButtons.forEach(button => {
        button.addEventListener('click', function() {
            formatButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const selectedFormat = this.dataset.format;
            updateDisplayFormat(selectedFormat);
        });
    });

    function updateDisplayFormat(format) {
        // Actualizar direcciones en la tabla de subredes (si existe)
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

        // Actualizar hosts válidos (nuevo selector para la estructura modificada)
        document.querySelectorAll('.host-badge').forEach(element => {
            const originalIP = element.textContent;
            element.textContent = convertIPFormat(originalIP, format);
        });

        // Actualizar direcciones de red y broadcast (nuevos selectores)
        const networkAddr = document.querySelector('.network-info [class*="font-monospace"]:first-child');
        const broadcastAddr = document.querySelector('.network-info [class*="font-monospace"]:last-child');
        
        if (networkAddr && broadcastAddr) {
            networkAddr.textContent = convertIPFormat(networkAddr.textContent, format);
            broadcastAddr.textContent = convertIPFormat(broadcastAddr.textContent, format);
        }
    }

    function convertIPFormat(ip, format) {
        if (!ip) return '';
        try {
            const octets = ip.split('.');
            switch(format) {
                case 'binario':
                    return octets.map(oct => parseInt(oct).toString(2).padStart(8, '0')).join('.');
                case 'hexadecimal':
                    return octets.map(oct => parseInt(oct).toString(16).padStart(2, '0')).join('.');
                default:
                    return ip;
            }
        } catch (e) {
            console.error("Error al convertir formato:", e);
            return ip;
        }
    }

    // =============================================
    // 2. Validación de Formularios (Actualizado)
    // =============================================
    const ipInputs = document.querySelectorAll('input[type="text"][name*="ip"]');
    ipInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9.]/g, '');
        });
    });
    
    const maskInputs = document.querySelectorAll('input[name*="mascara"]');
    maskInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9./]/g, '');
        });
    });
    
    const conexionesInput = document.getElementById('conexiones');
    if(conexionesInput) {
        conexionesInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9,]/g, '');
        });
    }

    // =============================================
    // 3. Nuevo: Manejo de pestañas y persistencia
    // =============================================
    const tabLinks = document.querySelectorAll('.nav-link');
    tabLinks.forEach(tab => {
        tab.addEventListener('click', function() {
            // Limpiar formatos activos al cambiar de pestaña
            formatButtons.forEach(btn => {
                if(btn.classList.contains('active')) {
                    btn.classList.remove('active');
                    document.querySelector('.format-btn[data-format="decimal"]').classList.add('active');
                    updateDisplayFormat('decimal');
                }
            });
        });
    });

    // =============================================
    // 4. Tooltips (Mejorado)
    // =============================================
    const infoIcons = document.querySelectorAll('.info-icon');
    infoIcons.forEach(icon => {
        new bootstrap.Tooltip(icon, {
            trigger: 'hover focus'
        });
    });
    // =============================================
    // 5. Control de visualización de pestañas (NUEVO)
    // =============================================
    const subnetTab = document.querySelector('#subnet-tab');
    const hostsTab = document.querySelector('#hosts-tab');
    const subnetContent = document.querySelector('#subnet-content');
    const hostsContent = document.querySelector('#hosts-content');

    // Función para actualizar el contenido visible
    function updateTabContent(activeTab) {
        if (activeTab === 'subnet') {
            if (subnetContent) subnetContent.style.display = 'block';
            if (hostsContent) hostsContent.style.display = 'none';
        } else if (activeTab === 'hosts') {
            if (subnetContent) subnetContent.style.display = 'none';
            if (hostsContent) hostsContent.style.display = 'block';
        }
    }

    // Event listeners para las pestañas
    if (subnetTab && hostsTab) {
        subnetTab.addEventListener('click', () => updateTabContent('subnet'));
        hostsTab.addEventListener('click', () => updateTabContent('hosts'));
    }

    // Inicializar según la pestaña activa al cargar
    const activeTab = document.querySelector('.nav-link.active').id;
    updateTabContent(activeTab.replace('-tab', ''));
    
    // Integración con Bootstrap tabs para sincronización
    const tabEls = document.querySelectorAll('button[data-bs-toggle="tab"]');
    tabEls.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', function(event) {
            const targetTab = event.target.id.replace('-tab', '');
            updateTabContent(targetTab);
        });
    });
});
