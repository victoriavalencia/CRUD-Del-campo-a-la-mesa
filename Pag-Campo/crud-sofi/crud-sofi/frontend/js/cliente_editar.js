console.log(location.search) // lee los argumentos pasados a este formulario
var id = location.search.substring(4)
console.log(id)
const {
    createApp
} = Vue
createApp({
    data() {
        return {
            id: 0,
            nombre: "",
            apellido: "",
            telefono: 0,
            localidad: "",
            direccion: "",
            bolson: 0,
            medio_de_pago: "",
            dia_de_entrega: "",

            url:'https://victoriatarabusi.pythonanywhere.com/clientes/' + id //ruta local
            //url: 'https://sofitarabusi.pythonanywhere.com/' + id //ruta pythonanywhere
        }
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.id = data.id
                    this.nombre = data.nombre;
                    this.apellido = data.apellido
                    this.telefono = data.telefono
                    this.localidad = data.localidad
                    this.direccion = data.direccion
                    this.bolson = data.bolson
                    this.medio_de_pago = data.medio_de_pago
                    this.dia_de_entrega = data.dia_de_entrega                   
                })
                .catch(err => {
                    console.error(err);
                    this.error = true
                })
        },
        modificar() {
            let cliente = {
                nombre: this.nombre,
                apellido: this.apellido,
                telefono: this.telefono,
                localidad: this.localidad,
                direccion: this.direccion,
                bolson: this.bolson,
                medio_de_pago: this.medio_de_pago,
                dia_de_entrega: this.dia_de_entrega
            }
            var options = {
                body: JSON.stringify(cliente),
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function() {
                    alert("Registro modificado")
                    window.location.href = "./clientes.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar")
                })
        }
    },
    created() {
        this.fetchData(this.url)
    },
}).mount('#app')