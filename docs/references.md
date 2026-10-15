# Referências — gráficos de movimento (2026-10-14)

- [Matplotlib: backends](https://matplotlib.org/stable/users/explain/figure/backends.html):
  Agg exporta arquivos; TkAgg usa Tkinter para janelas. Aplicação: detectar canvas
  sem GUI antes de executar ensaio ao vivo; preservar backends GUI funcionais.
  Reprodução e limites: [diagnóstico da janela](engineering-decisions/2026-10-14-janela-graficos.md).

- [Matplotlib: figuras interativas](https://matplotlib.org/stable/users/interactive.html):
  consultado para corrigir o fechamento automático ao final da coleta.
  `show(block=True)` mantém o processamento dos eventos da GUI até fechar as janelas,
  inclusive em modo interativo. Decisão: salvar PNG/CSV antes de esperar; manter
  `--no-live` sem espera. Teste automatizado verifica exportação antes de exibir e
  fechamento posterior; GUI real validada posteriormente no script
  `tools/check_plot_window.py`, hardware não validado. Reprodução:
  `python -m unittest discover -s tests -q`.

- [Hiwonder LX-225](https://www.hiwonder.com/products/lx-225): tabela oficial consultada.
  [DATASHEET] 115200 baud, 6–8,4 V, feedback de posição/tensão/temperatura e conversão
  0–1000 para 0–240°. A tabela explícita de protocolo foi adotada apesar da menção
  promocional a 270°. Não sustenta controle posicional de 360° nem medição de torque.
- [Manuais e protocolo](datasheets/README.md): referências preexistentes do driver;
  o protocolo serial não foi alterado nesta tarefa.
- Arquivo local `2.5 2servos`: inspeção estática, sem evidência de ensaio físico.
  Usado para comparação de interface e simplificação, não como datasheet.

Reprodução: instalar requirements.txt e rodar os testes sem hardware. Na bancada,
registrar fonte, carga, IDs, condições e CSV original. Hardware, carga e incerteza:
TODO: dado não disponível. Nenhum resultado físico foi fabricado.

## Instalação multiplataforma — 2026-10-14

Problema: orientar instalação/testes em Windows 10/11 e Ubuntu/derivados sem confundir
biblioteca Python com driver USB. Método: documentação oficial WCH, kernel Linux,
pySerial, Matplotlib e Hiwonder; links em [guia por sistema](windows-linux.md#fontes-oficiais).
Resultado: roteiro por sistema, identificação do chip, permissão serial, Tk/GUI,
testes de software e ensaio físico progressivo. Windows usa pacote oficial WCH quando
necessário; Linux prioriza driver do kernel. Não foi instalado driver nem aberto hardware.
Limites: versão exata do pacote WCH e revisão USB da montagem não verificadas;
nenhuma alegação de compatibilidade física validada por testes em CI.
Reprodução: executar o roteiro no sistema alvo e registrar versões, montagem e dados.

## Teste de velocidade e relógio — 2026-10-14

Problema: execução [38624539070](https://github.com/Pedronsjaja/gaia-lx225-buslinker/actions/runs/38624539070)
falhou no Windows/Python 3.12: `test_temperature_and_velocity` esperava zero e recebeu NaN.
O teste usava duas respostas seriais simuladas consecutivas e o relógio real.
O driver mantém NaN quando o intervalo é menor ou igual a 1 microsegundo.
Hipótese sustentada pelo código: as leituras podem compartilhar um instante do relógio;
o intervalo exato da execução original não foi registrado.

Método: controlar o relógio no teste com 10 e 10,25 s, mantendo a serial simulada.
Cobrir também instantes iguais (velocidade indisponível) e variação de 5 graus em
0,25 s (20 graus/s, CALCULADO). Não alterar o driver nem substituir NaN por zero.
Referência: [Python time.monotonic e resolução do relógio](https://docs.python.org/3/library/time.html#time.monotonic).
O relógio é monotônico, mas isso não garante um incremento entre chamadas consecutivas.

TESTADO AUTOMATICAMENTE no Windows/Python 3.13.14: 59 testes aprovados com
`python -m unittest discover -s tests -v`; `python -m pip check` aprovado.
`python tools/build_standalone.py` não alterou o conteúdo versionado dos gerados;
`--help` dos dois programas passou. NÃO TESTADO EM HARDWARE.
Os testes verificam lógica com dados simulados, não a exatidão física da velocidade.
