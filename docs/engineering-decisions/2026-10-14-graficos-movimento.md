# Gráficos durante movimentos — 2026-10-14

Comparação do arquivo `2.5 2servos` da Área de Trabalho com `origin/main`, commit
2ce2ffe. O original foi preservado como referência, sem executar seus movimentos.

## Diagnóstico e decisão

| Prioridade | Evidência | Decisão |
| --- | --- | --- |
| CRÍTICO | Compacto usa 360/1000; fabricante especifica 240/1000 | Preservar conversão oficial |
| ALTO | Blocos duplicados e erro de indentação na linha 514 | Não copiar exemplos executáveis |
| ALTO | Calibração compacta omite consulta de modo e limites | Preservar verificações do projeto |
| ALTO | Movimento do menu não grava nem verifica temperatura | Integrar Recorder e limite de 60 °C |
| MÉDIO | Gráficos restritos a monitor/calibrate | Integrar também ao menu e --move |
| BAIXO | IDs e portas fixos nos exemplos | Manter seleção explícita e descoberta |

Alternativas: substituir pelo compacto, duplicar gráficos ou integrar o gravador
existente. Escolhida a integração mínima: conserva protocolo, confirmação de comandos,
validações e testes; gera V2.5/V3 da mesma fonte, sem novas dependências.
A facilidade de trabalhar com um ou dois servos já existe no menu; mantivemos essa
interface sem presumir IDs nem limitar a quantidade de servos.

## Resultado e limites

Gráficos ao vivo por padrão nos movimentos; `--no-live` desativa a janela.
CSV bruto, PNG e comparação por ID são salvos em subpasta única de `--output`.
A leitura inicial precede o comando; há uma leitura explícita após a janela comandada
mais 0,5 s. Em interrupções, a última leitura pode ser parcial: veja `run_status`.
Sem segunda leitura válida, os campos finais recebem NaN. Alvo quantizado a 0,24°;
erro é posição menos alvo. `completed` significa conclusão da coleta, não estabilização.

[MEDIDO, quando conectado] posição, tensão e temperatura reportadas pelo servo.
[ESTIMADO] velocidade por diferenças de posição. [CALCULADO] erro e duração entre
amostras. Timestamp monotônico do computador associado à leitura de posição;
tensão e temperatura são consultadas sequencialmente, sem simultaneidade garantida.
A espera de 0,1 s soma-se aos tempos de comunicação e desenho; não garante 10 Hz.
Duração observada inclui preparo e não mede tempo de acomodação. Limite térmico
é política do ensaio. STOP não equivale a desligamento físico de emergência.
Feedback interno não substitui metrologia externa.

## Validação e próximos passos

`python -m unittest discover -s tests -v`: 52 testes passaram em 2026-10-14.
TESTADO AUTOMATICAMENTE com serial/dados simulados e geração de PNG.
NÃO TESTADO EM HARDWARE. Janela ao vivo ainda requer validação com backend GUI.
Nenhuma serial física foi aberta. Arquivos autônomos devem ser reproduzíveis por
`python tools/build_standalone.py`.

1. Concluído: integração, comparação e testes automáticos.
2. Próximo: operador confirmar montagem, fonte e limites; testar pequeno deslocamento em um servo.
3. Depois: repetir com dois servos e comparar queda de tensão e intervalos reais do CSV.
4. Com evidências: avaliar taxa de aquisição e desacoplamento da renderização.

Para entender esta implementação: siga `recorded_movement` → `test_movement` →
`Recorder`. Estude feedback versus referência, quantização e tempo comandado versus
observado. Desafio: calcular o intervalo mediano entre posições de cada ID no CSV.
Fontes: [referências](../references.md).
