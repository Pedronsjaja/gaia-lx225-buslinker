# Bancada LX-225

Driver em servo_testbench.py; CLI em test_servos.py; ensaios em bench_tools.py.
Editar esses fontes e regenerar ambos os arquivos autonomos com
`python tools/build_standalone.py`. Nao editar as copias geradas diretamente.

Antes de movimentos: consultar modo, limites, tensao e temperatura; validar
todos os alvos antes de enviar qualquer um. Nunca executar testes em serial
fisica sem montagem, alimentacao, limites mecanicos e operador confirmados.
Nao confundir limites internos do servo com seguranca mecanica.

Validacao: `python -m unittest discover -s tests -v` usa serial simulada.
Velocidade e ESTIMADA por diferenca de posicoes; feedback do servo nao e
referencia metrologica externa. Preservar CSV bruto e registrar montagem,
versao, unidades e condicoes em ensaios. Fontes: docs/datasheets e docs/gaia_lx225.md.
Definition of Done: regressao, gerados consistentes, documentacao dos limites
e nenhuma alegacao de TESTADO EM HARDWARE sem evidencia.
