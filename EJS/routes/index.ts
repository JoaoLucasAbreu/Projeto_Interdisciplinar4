import app = require("teem");

class IndexRoute {
	public async index(req: app.Request, res: app.Response) {
		res.render("index/index");
	}

	public async explore(req: app.Request, res: app.Response) {
		let artes: any[];

		await app.sql.connect(async (sql) => {

			artes = await sql.query("SELECT id_arte, titulo_arte, autor, tema, sobre FROM arte");

		});

		const opcoes = {
			artes: artes
		};

		res.render("index/explore", opcoes);
	}

	public async upload(req: app.Request, res: app.Response) {
		res.render("index/upload");
	}

	public async about(req: app.Request, res: app.Response) {
		res.render("index/about");
	}

	public async oi(req: app.Request, res: app.Response) {
		res.send("game play");
	}

	@app.http.post()
	public async criarUsuario(req: app.Request, res: app.Response) {
		// Os dados enviados via POST ficam dentro de req.body
		let pessoa = req.body;

		// É sempre muito importante validar os dados do lado do servidor,
		// mesmo que eles tenham sido validados do lado do cliente!!!
		if (!pessoa) {
			res.status(400);
			res.json("Dados inválidos");
			return;
		}

		if (!pessoa.nome) {
			res.status(400);
			res.json("Nome inválido");
			return;
		}

		if (!pessoa.sobrenome) {
			res.status(400);
			res.json("Nome inválido");
			return;
		}

		if (!pessoa.apelido) {
			res.status(400);
			res.json("Apelido inválido");
			return;
		}

		if (!pessoa.email) {
			res.status(400);
			res.json("E-mail inválido");
			return;
		}

		if (!pessoa.senha) {
			res.status(400);
			res.json("E-mail inválido");
			return;
		}

		await app.sql.connect(async (sql) => {

			// Todas os comandos SQL devem ser executados aqui dentro do app.sql.connect().

			// As interrogações serão substituídas pelos valores passados ao final, na ordem passada.
			await sql.query("INSERT INTO usuario (nome, sobrenome, apelido, email, senha) VALUES (?, ?, ?, ?, ?)", [pessoa.nome, pessoa.sobrenome, pessoa.apelido, pessoa.email, pessoa.senha]);

		});

		res.json(true);
	}

	@app.route.formData()
	@app.http.post()
	public async criarObra(req: app.Request, res: app.Response) {
		// Os dados enviados via POST ficam dentro de req.body
		let obra = req.body;

		if (!obra.titulo_arte) {
			res.status(400);
			res.json("Nome inválido");
			return;
		}

		if (!obra.autor) {
			res.status(400);
			res.json("Autor inválido");
			return;
		}

		if (!obra.tema) {
			res.status(400);
			res.json("Tema inválido");
			return;
		}

		if (!obra.sobre) {
			obra.sobre = "";
		}

		if (!req.uploadedFiles || !req.uploadedFiles.imagem) {
			res.status(400);
			res.json("Imagem inválida");
			return;
		}

		if (req.uploadedFiles.imagem.size > 1024 * 1024) {
			res.status(400);
			res.json("Imagem muito grande");
			return;
		}

		await app.sql.connect(async (sql) => {

			await sql.beginTransaction();

			// Todas os comandos SQL devem ser executados aqui dentro do app.sql.connect().

			// As interrogações serão substituídas pelos valores passados ao final, na ordem passada.
			await sql.query("INSERT INTO arte (titulo_arte, autor, tema, sobre) VALUES (?, ?, ?, ?)", [obra.titulo_arte, obra.autor, obra.tema, obra.sobre]);

			let id: number = await sql.scalar("SELECT last_insert_id()");

			await app.fileSystem.saveUploadedFileToNewFile("/public/IMGS/artes/arte" + id + ".jpg", req.uploadedFiles.imagem);

			await sql.commit();

		});

		res.json(true);
	}

}

export = IndexRoute;
