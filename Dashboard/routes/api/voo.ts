﻿import { sql } from "teem";
import app = require("teem");

/* class VooApiRoute {
	public static async listar(req: app.Request, res: app.Response) {

		const iddestino = parseInt(req.query["d"] as string) || 0;
		//const companhia = req.query["c"] || "";
		
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

export = VooApiRoute; */

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

	public static async top5(req: app.Request, res: app.Response) {
		let valores = null

		await sql.connect(async (sql) => {
			valores = await sql.query('SELECT voo.destino, voo.destinoSigla, tp_passagem.preco FROM passagem INNER JOIN voo ON passagem.idVoo = voo.idVoo INNER JOIN tp_passagem ON passagem.idPassagem = tp_passagem.idPassagem WHERE tp_passagem.tipoPassagem = "MAIOR" and  passagem.dataPesquisa = "2022-10-19" ORDER BY tp_passagem.preco DESC LIMIT 5');
		});

		let dados = {
			preco: valores.map( x => x.preco),
			siglas: valores.map( x => x.destinoSigla),
			destinos: valores.map( x => x.destibo),
			
		};
		
		res.json(dados);
	}
}

export = VooApiRoute;
