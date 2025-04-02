// Inicializar tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});
        
// Validación básica del formulario
document.getElementById('subnetForm').addEventListener('submit', function(e) {
    const ip = document.getElementById('ip').value;
    if (!/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(ip)) {
        alert('Por favor ingrese una dirección IP válida');
        e.preventDefault();
    }
});
        
// Cambiar entre formularios según la pestaña activa
document.getElementById('hosts-tab').addEventListener('click', function() {
    document.getElementById('host_ip').setAttribute('name', 'ip');
    document.getElementById('host_mascara').setAttribute('name', 'mascara');
    document.getElementById('conexiones').removeAttribute('name');
    document.getElementById('hosts').removeAttribute('name');
});
        
document.getElementById('subnet-tab').addEventListener('click', function() {
    document.getElementById('host_ip').removeAttribute('name');
    document.getElementById('host_mascara').removeAttribute('name');
    document.getElementById('conexiones').setAttribute('name', 'conexiones');
    document.getElementById('hosts').setAttribute('name', 'hosts');
});
