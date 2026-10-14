# Posição absoluta por ID no menu

Problema: a opção 4 aplicava o mesmo deslocamento relativo a todos os IDs.
O usuário precisa escolher uma posição diferente para cada servo.

Decisão: pedir os alvos absolutos individualmente e conservar tempo comum,
Recorder e envio direto em sequência rápida. Alternativa descartada: pedir
deslocamentos individuais, pois não expressa diretamente a posição desejada.
Não houve alteração do protocolo nem inclusão de dependências.

Todos os alvos passam pelas validações existentes antes de habilitar torque ou
enviar movimentos. Mantida a restrição de deslocamento de até 100° por ensaio,
inclusive para alvos absolutos. Os estados são relidos após a entrada dos alvos.
A opção 2 e o argumento --delta continuam relativos. CSV e gráficos associam
o alvo quantizado ao respectivo ID; a velocidade continua ESTIMADA.

Referências consultadas: [referências do driver](../references.md),
`LX225Bus._prepare_targets`, `move_group_direct` e `test_movement`.
A inspeção confirmou que o transporte existente já aceita alvos por ID;
o problema estava na interface e na preparação dos alvos.

Validação: `python tools/build_standalone.py` regenerou V2.5 e V3;
`python -m unittest discover -s tests -q`: 54 testes passaram.
TESTADO AUTOMATICAMENTE com mocks/serial simulada, incluindo menu dos dois
autônomos, alvos distintos no CSV/PNG e bloqueio do grupo com alvo inválido.
NÃO TESTADO EM HARDWARE nem janela GUI ao vivo. Limites internos não comprovam
segurança mecânica; montagem e carga: TODO: dado não disponível.

Para entender esta implementação: siga `interactive_menu` → `recorded_movement`
→ `test_movement` → `move_group_direct`. Estude posição absoluta versus
deslocamento relativo e quantização. Próximo passo: validar em bancada com
operador e percurso confirmados, preservando o CSV original.
