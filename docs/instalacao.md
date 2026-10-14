# Instalação e primeiro uso

[Voltar ao README](../README.md) · [Downloads](softwares-e-drivers.md) · [Problemas](solucao-de-problemas.md)

## 1. Separe e conecte o material

| Material | Conferir |
| --- | --- |
| BusLinker V2.5 ou V3.0 | Revisão impressa na placa e seleção de comunicação |
| Um LX-225 e cabo de servo | Cabo íntegro e eixo com percurso livre |
| Fonte externa | 6–8,4 V no LX-225, polaridade e corrente adequadas |
| USB de dados | Conector da revisão; V3 usa USB-C |
| Computador | Python e porta USB disponíveis |

Faça as conexões com a fonte desligada. Confira alimentação, terra comum e sinal pelos rótulos e [diagramas da revisão](datasheets/README.md), não apenas pela cor do cabo. A fonte alimenta os servos; não use só o USB como alimentação de potência.

**Ajuste também o limite de corrente da fonte/regulador.** Nos testes da equipe, pedidos de delta de +100 ou +200 em apenas 1 s ou 0,5 s provocavam queda de tensão no servo. O limite de corrente estava ajustado no mínimo: quando o movimento exigia mais corrente, a fonte atingia esse limite e a tensão de saída caía.

Antes de testar movimentos, ajuste o limite de corrente conforme a necessidade do servo e a capacidade da fonte e dos cabos, mantendo a tensão entre 6 e 8,4 V. Comece com deslocamentos pequenos e lentos e acompanhe a tensão durante o movimento. Os deltas acima descrevem o ocorrido na bancada; o comando `--delta` deste projeto aceita apenas de −100 a +100 graus, respeitando também os limites de posição do servo.

Na V3, o manual de servos padrão indica a seleção **Servo/USB**. Veja a figura do manual antes de colocar os jumpers. Não copie posições físicas entre revisões. Os exemplos com 11,1/12 V do manual são para outros servos: **não aplique essa tensão ao LX-225**.

## 2. Instale Python e baixe o projeto

Instale Python 3.9 ou superior pelo [site oficial](https://www.python.org/downloads/) e habilite a inclusão no PATH, se oferecida. Abra um terminal novo:

```powershell
python --version
```

No GitHub, use **Code → Download ZIP**, extraia tudo e abra a pasta que contém `README.md` e `requirements.txt` no VS Code ou terminal.

## 3. Prepare o ambiente no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import serial, matplotlib; from servo_testbench import LX225Bus; print('Instalacao OK')"
```

O resultado esperado é `Instalacao OK`.

Para executar os exemplos curtos do manual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, use `.\.venv\Scripts\python.exe` no lugar de `python`; não é necessário mudar a política do sistema. No VS Code, escolha **Python: Select Interpreter** e selecione o Python de `.venv`.

## 4. Identifique a porta USB

1. Conecte a placa com um cabo USB de dados.
2. Abra **Gerenciador de Dispositivos → Portas (COM e LPT)**.
3. Se o conversor CH340/CH341 estiver sem driver, siga [CH341SER](softwares-e-drivers.md). Se já funcionar, não precisa reinstalar.
4. Anote a COM. Desconectar e reconectar o USB ajuda a identificar a entrada correspondente.

```powershell
.\.venv\Scripts\python.exe -m serial.tools.list_ports -v
```

`COM7` é apenas exemplo; substitua nos comandos. A presença da COM confirma o conversor USB, não a comunicação com o servo.

## 5. Faça a primeira leitura

Com um único servo conectado conforme a etapa 1, ligue a fonte. Feche Bus Servo Terminal, ServoStudio e monitores seriais que possam ocupar a porta.

```powershell
.\.venv\Scripts\python.exe buslinker_v3.py --port COM7 --scan
```

Na V2.5, use `buslinker_v2_5.py`. A busca percorre 0–253, pode levar cerca de 12 segundos e não altera configurações. Espere um ID com posição, tensão e temperatura válidas. Para consultar um ID conhecido:

```powershell
.\.venv\Scripts\python.exe buslinker_v3.py --port COM7 --ids 1
```

O ID de fábrica do LX-225 é 1, mas pode ter sido alterado. Se nenhum servo responder, siga o [diagnóstico](solucao-de-problemas.md) antes de mover.

## 6. Teste movimento e monitoramento

Depois de conferir o percurso mecânico, e supondo ID 1:

```powershell
.\.venv\Scripts\python.exe buslinker_v3.py --port COM7 --ids 1 --move --delta 5 --seconds 2
```

O deslocamento é relativo à posição atual. O alvo precisa respeitar limites internos e mecânicos. Não há retorno automático. A tentativa de parada por software depende da comunicação; fechar a serial não desliga torque.

Para gráficos sem movimento:

```powershell
.\.venv\Scripts\python.exe buslinker_v3.py monitor --port COM7 --ids 1 --duration 30 --live
```

## 7. Monte o barramento com mais servos

Configure IDs exclusivos **um servo por vez**, usando [change-id](uso.md). `add-id` só cadastra nomes no computador. Desligue a alimentação, interligue os servos, dimensione a alimentação do conjunto e consulte todos antes de testar movimento múltiplo.

## Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m serial.tools.list_ports -v
```

Use a porta encontrada, como `/dev/ttyUSB0` ou `/dev/cu.usbserial-...`. No Ubuntu/Debian, instale `python3-venv` se o sistema indicar ausência. Para permissão serial, consulte `ls -l /dev/ttyUSB0`; se o grupo for `dialout`, use `sudo usermod -aG dialout "$USER"` e faça logout/login. Evite executar a bancada como root.

O [fabricante WCH](https://www.wch-ic.com/downloads/CH341SER.EXE.html?type=en) também disponibiliza pacotes Linux/macOS. Confira primeiro se o sistema já reconhece o conversor. Essas plataformas não foram verificadas em hardware neste trabalho.

## Roteiros completos por sistema

Veja [Windows 10/11 e Ubuntu/Linux](windows-linux.md) para comandos completos, dependência Tk dos gráficos, testes sem hardware e sequência de ensaio com um ou vários servos.
