async function verificarAutenticacion() {
    const response = await fetch('http://127.0.0.1:8000/user/me', {
        method: 'GET',
        headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
    window.data = await response.json();
    data = window.data
    if (!response.ok || data.error) {
        window.location.href = 'http://127.0.0.1:8000/Skillmap/';
    }else{
        document.querySelector('header').style.opacity = 1;
        try {
            const response = await fetch(`http://127.0.0.1:8000/resultados/?correo=${encodeURIComponent(data.correo)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            data = await response.json();
            if (data.exito){
                console.log("entramos a data.exito: ", data.exito)
                const resultsContainer = document.createElement('div');
                resultsContainer.id = 'resultsContainer';
                document.body.appendChild(resultsContainer); // Añade el contenedor al cuerpo del documento

                // Itera sobre cada carrera en el objeto `exito`
                for (let i = 1; i <= 8; i++) {
                    const carreraKey = `id_carrera${i}`;
                    const carreraInfo = data.exito[carreraKey];

                    if (carreraInfo) {
                        // Crea un nuevo div para cada carrera y añade la información
                        const carreraDiv = document.createElement('div');
                        carreraDiv.classList.add('carrera');
                        carreraDiv.innerHTML = `<h2>Carrera ${i}</h2><p>${carreraInfo}</p>`;

                        // Añade el div de la carrera al contenedor de resultados
                        resultsContainer.appendChild(carreraDiv);
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}
verificarAutenticacion();

document.addEventListener('DOMContentLoaded', () => {
    const cerrarSesionBtn = document.getElementById('cerrar_sesion');
    if (cerrarSesionBtn) {
        cerrarSesionBtn.addEventListener('click', function() {
            localStorage.removeItem('access_token');
            window.location.href = 'http://127.0.0.1:8000/Skillmap/';
        });
    } else {
        console.error('El botón con id "cerrar_sesion" no se encontró.');
    }
});