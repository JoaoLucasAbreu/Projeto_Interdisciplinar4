import app = require("teem");

class dados {
    static listar_destinos() {
            return app.sql.connect(async (sql) => {
                return (await sql.query("select destino from voo order by destino asc")) || [];
            });
    }
}

export = dados;