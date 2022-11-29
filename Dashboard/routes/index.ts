import app = require("teem");
import Usuario = require("../models/usuario");

class IndexRoute {
	public static async index(req: app.Request, res: app.Response) {
		let u = await Usuario.cookie(req);
		if (!u) {
			res.redirect(app.root + "/login");
		} else {
			let maiores: any[];
			let destinos: any[];
			await app.sql.connect(async (sql) => {
				destinos = await sql.query("SELECT idVoo, destino FROM voo ORDER BY destino ASC");
				maiores = await sql.query('SELECT distinct passagem.media, voo.destino, voo.destinoSigla FROM passagem INNER JOIN voo ON passagem.idVoo = voo.idVoo group by voo.destino ORDER BY passagem.media DESC');
			});

			let passagens: any[];
			await app.sql.connect(async (sql) => {
				passagens = await sql.query("SELECT voo.destino, tp_passagem.preco, tp_passagem.tipoPassagem, tp_passagem.hSaida, tp_passagem.duracao, passagem.companhia, passagem.dataPesquisa FROM passagem INNER JOIN voo ON passagem.idVoo = voo.idVoo INNER JOIN tp_passagem ON passagem.idPassagem = tp_passagem.idPassagem WHERE tp_passagem.tipoPassagem = ? and passagem.dataPesquisa = ?", ["MENOR","2022-10-19"]) as [] ; 
			});


			res.render("index/index", {
				layout: "layout-sem-form",
				titulo: "Dashboard",
				usuario: u,
				destinos: destinos,
				passagens: passagens,
				maiores: maiores
			});
		}
	}

	@app.http.all()
	public static async login(req: app.Request, res: app.Response) {
		let u = await Usuario.cookie(req);
		if (!u) {
			let mensagem: string = null;
	
			if (req.body.email || req.body.senha) {
				[mensagem, u] = await Usuario.efetuarLogin(req.body.email as string, req.body.senha as string, res);
				if (mensagem)
					res.render("index/login", {
						layout: "layout-externo",
						mensagem: mensagem
					});
				else
					res.redirect(app.root + "/");
			} else {
				res.render("index/login", {
					layout: "layout-externo",
					mensagem: null
				});
			}
		} else {
			res.redirect(app.root + "/");
		}
	}

	public static async acesso(req: app.Request, res: app.Response) {
		let u = await Usuario.cookie(req);
		if (!u)
			res.redirect(app.root + "/login");
		else
			res.render("index/acesso", {
				layout: "layout-sem-form",
				titulo: "Sem Permissão",
				usuario: u
			});
	}

	public static async perfil(req: app.Request, res: app.Response) {
		let u = await Usuario.cookie(req);
		if (!u)
			res.redirect(app.root + "/");
		else
			res.render("index/perfil", {
				titulo: "Meu Perfil",
				usuario: u
			});
	}

	public static async logout(req: app.Request, res: app.Response) {
		let u = await Usuario.cookie(req);
		if (u)
			await Usuario.efetuarLogout(u, res);
		res.redirect(app.root + "/");
	}
}

export = IndexRoute;
