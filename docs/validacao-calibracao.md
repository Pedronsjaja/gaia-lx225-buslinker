# Prevalidacao da calibracao

O comando `calibrate` consulta modo de posicao e limites internos de cada ID
antes de qualquer movimento. Um alvo fora dos limites, modo motor ou timeout
aborta o lote inteiro. Os alvos sao quantizados em passos de 0,24 grau antes
da comparacao, conforme o protocolo ja implementado no driver.

TESTADO AUTOMATICAMENTE: serial falsa, incluindo plano cujo primeiro alvo e
valido e o segundo invalido. NAO TESTADO EM HARDWARE nesta alteracao.
Referencia: protocolo LX-225 em docs/datasheets e comandos 21/30 do driver.

Limites mecanicos da montagem: UNKNOWN. Referencia angular externa,
incerteza, carga e repetibilidade fisica: NOT_MEASURED. O ensaio compara alvo
com feedback interno; nao determina exatidao absoluta nem autoriza movimento
em um robo montado. A parada por software depende da comunicacao funcionar.

Proximo passo: registrar uma unica junta, limites mecanicos confirmados,
fonte e limite de corrente, parada fisica e referencia externa. Depois,
executar ensaio supervisionado e preservar dados brutos e condicoes.

Para entender esta implementacao: acompanhe sample → plans → consultas →
move_many → amostragem → stop_all. Estude quantizacao, erro de indicacao,
repetibilidade e diferenca entre limite de firmware e limite mecanico.
Desafio: simule falha no segundo ID e confirme ausencia de comandos de movimento.
