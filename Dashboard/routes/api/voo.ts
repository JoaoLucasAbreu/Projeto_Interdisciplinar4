import { sql } from "teem";
import app = require("teem");

/*class VooApiRoute {
	public static async listar(req: app.Request, res: app.Response) {

		const iddestino = parseInt(req.query["d"] as string) || 0;
		const companhia = req.query["c"] || "";
		
		let labelsGol = null
		let labelsLatam = null
		let valoresGol = null
		let valoresLatam = null

		await sql.connect(async (sql) => {
			labelsGol = await sql.query('select distinct DATE_FORMAT(dataPesquisa,"%e/%m") AS dataPesquisa from passagem  where companhia = 1 and idVoo = ? ' ,[iddestino]) as [] ;
			labelsLatam = await sql.query('select distinct DATE_FORMAT(dataPesquisa,"%e/%m") AS dataPesquisa from passagem  where companhia = 2 and idVoo = ? ' ,[iddestino]) as [] ;
			valoresGol = await sql.query("select media from passagem where companhia = 1 and idVoo = ? ", [iddestino]) as [] ; 
			valoresLatam = await sql.query("select media from passagem where companhia = 2 and idVoo = ? ", [iddestino]) as [] ; 
		});

		let dados = {
			labelsGol: labelsGol.map( x => x.dataPesquisa),
			labelsLatam: labelsLatam.map( x => x.dataPesquisa),
			valoresGol: valoresGol.map( x => x.media),
			valoresLatam: valoresLatam.map( x => x.media),
			
		};

		console.log(dados);
		
		res.json(dados);
	}
}

export = VooApiRoute;*/

class VooApiRoute {
	public static async listar(req: app.Request, res: app.Response) {

		const iddestino = parseInt(req.query["d"] as string) || 0;
		//const companhia = req.query["c"] || "";
		
		let labelsGol = null
		let labelsLatam = null
		let valoresGol = null
		let valoresLatam = null

		await sql.connect(async (sql) => {
			labelsGol = await sql.query('select distinct DATE_FORMAT(dataPesquisa,"%e/%m") AS dataPesquisa from passagem  where companhia = ? and idVoo = ? ' ,["GOL",iddestino]) as [] ;
			labelsLatam = await sql.query('select distinct DATE_FORMAT(dataPesquisa,"%e/%m") AS dataPesquisa from passagem  where companhia = ? and idVoo = ? ' ,["LATAM",iddestino]) as [] ;
			valoresGol = await sql.query("select media from passagem where companhia = ? and idVoo = ? ", ["GOL",iddestino]) as [] ; 
			valoresLatam = await sql.query("select media from passagem where companhia = ? and idVoo = ? ", ["LATAM",iddestino]) as [] ; 
		});

		let dados = {
			labelsGol: labelsGol.map( x => x.dataPesquisa),
			labelsLatam: labelsLatam.map( x => x.dataPesquisa),
			valoresGol: valoresGol.map( x => x.media),
			valoresLatam: valoresLatam.map( x => x.media),
		};
		
		res.json(dados);
	}

	public static async regioes( res: app.Response) {
		let preco = null
		let regioes = null

		await sql.connect(async (sql) => {
			preco = await sql.query("SELECT avg(passagem.media) as preco FROM passagem INNER JOIN voo on passagem.idVoo = voo.idVoo GROUP BY voo.regiao;"); 
			regioes = await sql.query("SELECT voo.regiao FROM passagem INNER JOIN voo on passagem.idVoo = voo.idVoo GROUP BY voo.regiao;"); 
		});

		let dados = {
			regioes: regioes.map( x => x.regiao),
			preco: preco.map( x => x.preco),		
		};
		
		res.json(dados);
	}

	public static async regioes_media( res: app.Response) {
		
		let regioes_media = null;

		await sql.connect(async (sql) => {
			regioes_media = await sql.query("SELECT voo.regiao as regiao, avg(passagem.media) as preco FROM passagem INNER JOIN voo on passagem.idVoo = voo.idVoo GROUP BY voo.regiao;") ; 

		});
	
		let dados = {
			regioes: regioes_media.map( x => x.regiao),
			preco: regioes_media.map( x => x.preco),		
		};

		res.json(dados);
	}

}

export = VooApiRoute;
