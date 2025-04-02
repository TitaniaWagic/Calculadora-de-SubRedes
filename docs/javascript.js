// Validación de formularios
        document.addEventListener('DOMContentLoaded', function() {
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
        });
