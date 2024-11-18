async function verificarAutenticacion() {
let contResA = 0
let contResB = 0
let contResC = 0
let contResD = 0
let act1 = 0
let act2 = 0
let act3 = 0
let act4 = 0
var A1 = document.getElementById("A_1");
var A2 = document.getElementById("A_2");
var A3 = document.getElementById("A_3");
var B1 = document.getElementById("B_1");
var B2 = document.getElementById("B_2");
var B3 = document.getElementById("B_3");
var C1 = document.getElementById("C_1");
var C2 = document.getElementById("C_2");
var C3 = document.getElementById("C_3");
var D1 = document.getElementById("D_1");
var D2 = document.getElementById("D_2");
var D3 = document.getElementById("D_3");
var RA1 = document.getElementById("A1");
var RA2 = document.getElementById("A2");
var RA3 = document.getElementById("A3");
var RB1 = document.getElementById("B1");
var RB2 = document.getElementById("B2");
var RB3 = document.getElementById("B3");
var RC1 = document.getElementById("C1");
var RC2 = document.getElementById("C2");
var RC3 = document.getElementById("C3");
var RD1 = document.getElementById("D1");
var RD2 = document.getElementById("D2");
var RD3 = document.getElementById("D3");
const nombre = document.getElementById('nombre');
const correo = document.getElementById('email');
const response = await fetch('http://127.0.0.1:8000/user/me', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
});
const data = await response.json();
if (!response.ok || data.error) {
    window.location.href = 'http://127.0.0.1:8000/Skillmap/';
}else{
    document.querySelector('header').style.opacity = 1;
    nombretxt = "Nombre: "+data.name+" "+data.surname
    correotxt = "Correo: "+data.correo
    nombre.textContent = nombretxt
    correo.textContent = correotxt
    try {
        const response = await fetch(`http://127.0.0.1:8000/answers?correo=${encodeURIComponent(data.correo)}`, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
        });
        const respuestasUsuario = await response.json();
        for (const [pregunta, respuesta] of Object.entries(respuestasUsuario)) {
        if(respuesta == "A"){
            contResA+=1
        } else if(respuesta == "B"){
            contResB+=1
        } else if(respuesta == "C"){
            contResC+=1
        } else if(respuesta == "D"){
            contResD+=1
        } else if(pregunta == "formulario" && respuesta == true) {
            val = true;
        } else if(pregunta == "act1"){
            act1 = respuesta;
        } else if(pregunta == "act2"){
            act2 = respuesta;
        } else if(pregunta == "act3"){
            act3 = respuesta;
        } else if(pregunta == "act4"){
            act4 = respuesta;
        }
        }
        contResA = (contResA*3) + act1;
        contResB = (contResB*3) + act2;
        contResC = (contResC*3) + act3;
        contResD = (contResD*3) + act4;
        if (contResA >= contResB && contResA >= contResC && contResA >= contResD && val==true) {
        A1.style.display = "block";
        A2.style.display = "block";
        A3.style.display = "block";
        RA1.style.display = "block";
        RA2.style.display = "block";
        RA3.style.display = "block";
        } else if (contResB >= contResA && contResB >= contResC && contResB >= contResD && val==true) {
        B1.style.display = "block";
        B2.style.display = "block";
        B3.style.display = "block";
        RB1.style.display = "block";
        RB2.style.display = "block";
        RB3.style.display = "block";
        } else if (contResC >= contResA && contResC >= contResB && contResC >= contResD && val==true) {
        C1.style.display = "block";
        C2.style.display = "block";
        C3.style.display = "block";
        RC1.style.display = "block";
        RC2.style.display = "block";
        RC3.style.display = "block";
        } else if (contResD >= contResA && contResD >= contResB && contResD >= contResC && val==true){
        D1.style.display = "block";
        D2.style.display = "block";
        D3.style.display = "block";
        RD1.style.display = "block";
        RD2.style.display = "block";
        RD3.style.display = "block";
        }
    } catch (error) {
        console.error('Error al cargar respuestas:', error.message);
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