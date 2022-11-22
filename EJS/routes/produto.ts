import app = require("teem");

class ProdutoRoute {
	public async criar(req: app.Request, res: app.Response) {
		res.render("index/index");
	}

	public async alterarPreco(req: app.Request, res: app.Response) {
		res.send("Eu sou um texto...");
	}

	public async listar(req: app.Request, res: app.Response) {
		res.send("game play");
	}

    public async excluir(req: app.Request, res: app.Response) {
		res.send("game play");
	}
}

export = ProdutoRoute;
