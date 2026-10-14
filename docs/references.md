# Referências — gráficos de movimento (2026-10-14)

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
