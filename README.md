# Projeto_Interdisciplinar 4
Projeto : Quando eu voo
ESPM Sistemas de Informação, 4° Semestre

Web Scraper bimodal, no qual realiza a raspagem de dados úteis sobre valores, datas e horários de passagens das empresas GOL e LATAM.
O programa deve ser rodado na classe main.py, lembre-se anteriormente de subir o banco no MySQL e inserir os valores fixos de voo.

Para Fazer:
    - Arrumar webscraping_ltm.py;
    - Adicionar campo "tipo" na tabela tipo passagem ("MAIOR", "MENOR"), para auxiliar a filtragem de dados futuramente na dashboard;
    - Apagar as funções inúteis na storage.py;
    - Substituir a branch main pela mysql (precisa estar com os dois scrapings finalizados);
    - Subir a pasta ejs;
    - Idealizar as Dashboards;

Anotações:
    - Se rodar debugando ele pega todos os dados necessários, se rodar direto depois de um tempo ele devolve dados vazios ou números gigantes (geralmente perto da cidade "FOR").


SQL:
    SELECT voo.destino, tp_passagem.preco, tp_passagem.tipoPassagem, tp_passagem.hSaida, tp_passagem.duracao, passagem.companhia, passagem.dataPesquisa
    FROM passagem
    INNER JOIN voo ON passagem.idVoo = voo.idVoo
    INNER JOIN tp_passagem ON passagem.idPassagem = tp_passagem.idPassagem
    WHERE tp_passagem.tipoPassagem = "MENOR" and  passagem.dataPesquisa = "2022-10-19";

    SELECT voo.destino, tp_passagem.preco, tp_passagem.tipoPassagem
    FROM passagem
    INNER JOIN voo ON passagem.idVoo = voo.idVoo
    INNER JOIN tp_passagem ON passagem.idPassagem = tp_passagem.idPassagem
    WHERE tp_passagem.tipoPassagem = "MAIOR" and  passagem.dataPesquisa = "2022-10-19"
    ORDER BY tp_passagem.preco DESC
    LIMIT 5;

    SELECT voo.regiao, avg(passagem.media)
    FROM passagem
    INNER JOIN voo on passagem.idVoo = voo.idVoo
    GROUP BY voo.regiao;