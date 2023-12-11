const { createApp } = Vue
    createApp({
        data() {
            return {
                clientes: [],
                //url:'http://127.0.0.1:5000/clientes', // si el backend esta corriendo local usar localhost 5000
                url:'https://victoriatarabusi.pythonanywhere.com/clientes', // si ya lo subieron a pythonanywhere
                error: false,
                cargando: true,
                /*atributos para el guardar los valores del formulario */
                id: 0,
                nombre: "",
                apellido: "",
                telefono: 0,
                localidad: "",
                direccion: "",
                bolson: 0,
                medio_de_pago: "",
                dia_de_entrega: ""
            }
            },
            methods: {
                fetchData(url) {
                    fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        this.clientes = data;
                        this.cargando = false
                    })
                    .catch(err => {
                        console.error(err);
                        this.error = true
                    })
            },

            eliminar(cliente){
                const isConfirmed= window.confirm("¿Está seguro que desea eliminar este registro?");

                if(isConfirmed){
                    const url=this.url + '/' + cliente;
                    var options = {
                        method: 'DELETE'
                    };

                    fetch(url, options)
                        .then(res=> res.json())
                        .then(res=> {
                            location.reload();
                        })
                }
            },



            //REEMPLAZO ESTE ELIMINAR POR UNO QUE TENGA UN PROMPT DE CONFIRMACIÓN.
            // eliminar(cliente) {
            //     const url = this.url + '/' + cliente;
            //     var options = {
            //         method: 'DELETE',
            //     }

                
            //     fetch(url, options)
            //     .then(res => res.json()) // or res.json()
            //     .then(res => {
            //         location.reload();
            //     })
            // },
            grabar() {
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
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                redirect: 'follow'
                }
                fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./clientes.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabar")
                })
            }
        },
        created() {
            this.fetchData(this.url)
        },
    }).mount('#app')