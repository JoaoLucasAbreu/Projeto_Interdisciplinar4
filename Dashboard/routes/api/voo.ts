import { sql } from "teem";
import app = require("teem");

class VooApiRoute {
	public static async listar(req: app.Request, res: app.Response) {

		const iddestino = parseInt(req.query["d"] as string) || 0;
		const companhia = req.query["c"] || "";
		
		let labels = null
		let valores = null

		await sql.connect(async (sql) => {
			labels = await sql.query("select distinct dataPesquisa from passagem where companhia = ? and idVoo = ? " ,[companhia,iddestino]) as [] ;
			valores = await sql.query("select media from passagem where companhia = ? and idVoo = ? ", [companhia,iddestino]) as [] ; 
		});

		let dados = {
			labels: labels.map( x => x.dataPesquisa),
			valores: valores.map( x => x.media),
		};

		res.json(dados);
	}
}

export = VooApiRoute;
