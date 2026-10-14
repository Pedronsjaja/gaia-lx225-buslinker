# Diagnóstico e correção da janela de gráficos

## Problema e evidências

O usuário relatou ausência dos gráficos. [NÃO VERIFICADO] qual cópia e ambiente
produziram a última falha: não havia processo Python ativo para identificar.
Havia uma cópia antiga em `gaia-lx225-buslinker-main` sem gravação no menu.
Inspeção confirmou que `Recorder.close()` fechava a janela imediatamente após
salvar PNG. Um teste com backend Agg confirmou outro caso: modo de exportação
não abre janela, mesmo com a opção live. Não se atribui uma causa única ao relato.

## Decisão

Preservar gravação e aquisição; salvar arquivos antes da espera por fechamento.
Detectar canvas sem GUI e tentar TkAgg no modo live; avisar e falhar antes de
movimentar se a janela não puder ser criada. Manter --no-live sem janela.
Alternativa rejeitada: forçar TkAgg sempre, substituindo backends GUI funcionais.
Imprimir caminho do programa, backend e pasta de saída para distinguir cópias.
Adicionar --plot-test sem serial, com dados rotulados SIMULADOS no título e CSV.
Regenerar V2.5/V3 pela ferramenta existente, sem nova dependência.

## Validação em 2026-10-14

- `python -m unittest discover -s tests -q`: 57 testes passaram.
- `python tools/check_plot_window.py`: GUI_OK no módulo compartilhado e nos
  autônomos V2.5/V3. Forçado Agg antes de cada inicialização; recuperado TkAgg.
  Verificados quatro painéis com curvas de dois IDs simulados, `winfo_viewable()`,
  callback temporizado processado pelo loop GUI e PNG não vazio.
- Ambiente observado: Windows, Python 3.13, Matplotlib 3.11.1, Tk 8.6.

TESTADO AUTOMATICAMENTE, incluindo janelas reais em sessão desktop. Dados
SIMULADOS. NÃO TESTADO EM HARDWARE; não foi aberta porta serial. O teste de
janela não prova visibilidade em outro computador, ambiente Python ou sessão
sem desktop. O script fecha as janelas automaticamente após verificar eventos.

Para entender esta implementação: siga Recorder.__init__ → draw → close.
Estude backend gráfico versus exportação e loop de eventos da GUI.
Próximo passo: executar --plot-test no mesmo Python usado pelo operador;
depois validar aquisição real com montagem e percurso confirmados.

Fonte: [Matplotlib: backends](https://matplotlib.org/stable/users/explain/figure/backends.html)
e [figuras interativas](https://matplotlib.org/stable/users/interactive.html).
