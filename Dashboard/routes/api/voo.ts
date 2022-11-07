import { sql } from "teem";
import app = require("teem");

class VooApiRoute {
	public static async listar(req: app.Request, res: app.Response) {

		const iddestino = parseInt(req.query["d"] as string) || 0;
		const companhia = req.query["c"] || "";
		
		
		let labels = null;
		let valores = null;

		await sql.connect(async (sql) => {
	
			labels = await sql.query("select dataPesquisa from passagem where idVoo = ? and companhia = ?", [iddestino,companhia]);
			valores = await sql.query("select media from passagem where companhia = ? and idVoo = ?", [companhia,iddestino]);
		});

		let dados = {
			labels: labels,
			valores: valores
		};

		res.json(dados);
	}
}

export = VooApiRoute;
