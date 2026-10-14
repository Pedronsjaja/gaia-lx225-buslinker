# Windows 10/11, Ubuntu e distribuições semelhantes

[README](../README.md) · [Downloads oficiais](softwares-e-drivers.md) · [Montagem](instalacao.md)

Os mesmos `buslinker_v2_5.py` e `buslinker_v3.py` funcionam com a interface serial
multiplataforma do pySerial. Não existe firmware Windows/Linux para instalar no LX-225.
A placa precisa de um driver USB do sistema; os programas precisam de Python,
pyserial e matplotlib. A revisão BusLinker não determina sozinha o chip USB.

## Escolha do sistema e downloads

| Sistema | Driver USB CH340/CH341 | Ambiente Python e gráficos |
| --- | --- | --- |
| Windows 10/11 | [WCH CH341SER.EXE](https://www.wch.cn/downloads/ch341ser_exe.html), se a porta não funcionar | [Python para Windows](https://www.python.org/downloads/windows/), com Tcl/Tk; requirements.txt |
| Ubuntu / Debian | Driver `ch341` do kernel; normalmente não precisa baixar instalador | Pacotes python3, python3-venv e python3-tk; requirements.txt em venv |
| Linux Mint / Pop!_OS e derivados de Ubuntu/Debian | Mesmo caminho, conforme kernel e grupos da distribuição | Procedimento apt abaixo; verificar disponibilidade na versão instalada |
| Outras distribuições Linux | Conferir suporte `ch341` e grupo da porta | Instalar Python, suporte venv e Tk pelo gerenciador da distribuição; depois usar venv |

Use o pacote atual oferecido pelo fabricante e registre versão/data em cada ensaio.
Não fixamos uma versão numérica do CH341SER: a página oficial pode atualizar o pacote.
O fabricante lista Windows 10/11; isso não certifica todas as arquiteturas e revisões
USB. Para Windows ARM, confirme a arquitetura explicitamente no pacote antes de instalar.
Não instale CH341SER se a identificação mostrar outro conversor.

Bus Servo Terminal é uma ferramenta opcional distribuída como instalador Windows;
ServoStudio não é requisito do LX-225. Para Linux, o caminho documentado aqui é Python;
compatibilidade de aplicativos Windows via Wine não foi verificada.

## Windows 10/11 — instalação

1. No Gerenciador de Dispositivos, compare a lista antes/depois de conectar a placa.
2. Confira Propriedades → Detalhes → IDs de Hardware e o nome do conversor.
3. Para CH340/CH341 sem driver, baixe CH341SER pelo link oficial, execute o instalador
   e reconecte. Se a porta já funciona, não reinstale apenas por ter trocado de script.
4. Instale Python 3.12 ou 3.13 com Tcl/Tk e o launcher `py`, e extraia o repositório.
5. Abra PowerShell na pasta que contém requirements.txt:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m serial.tools.list_ports -v
```

Se `py` não existir, use o executável `python` da instalação escolhida.
O uso direto do Python de .venv dispensa mudar a política de execução do PowerShell.
Anote a COM real e a versão do driver na aba Driver do Gerenciador de Dispositivos.

## Ubuntu / Debian / Mint / Pop!_OS — instalação

Em uma instalação com apt, execute na pasta do projeto:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip python3-tk usbutils
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
lsusb
.venv/bin/python -m serial.tools.list_ports -v
```

Use Python 3.10 ou superior nesse roteiro; a matriz automática utiliza 3.12 e 3.13.
Não instale as dependências no Python do sistema usando sudo pip ou
`--break-system-packages`. Em outras distribuições, adapte apenas os pacotes do
sistema e o grupo serial; os comandos de venv e dos programas são os mesmos.

Para CH340/CH341, o kernel Linux fornece `ch341`. Se não surgir porta, investigue:

```bash
uname -r
lsusb
modinfo ch341
sudo journalctl -k -n 80 --no-pager
```

Se o módulo estiver disponível mas não carregado, tente `sudo modprobe ch341` e
reconecte. Se `modinfo` não o encontrar, pode ser driver embutido ou pacote/configuração
do kernel; consulte os pacotes oficiais da distribuição. Não substitua um driver
funcional por um módulo baixado/compilado sem diagnóstico.

Depois de identificar a porta real (ttyUSB0 é exemplo):

```bash
ls -l /dev/ttyUSB0
id -nG
```

Se o grupo da porta for `dialout` e seu usuário não fizer parte dele:

```bash
sudo usermod -aG dialout "$USER"
```

Faça logout/login completo e confira `id -nG` novamente. Outros sistemas podem usar
outro grupo: siga o grupo efetivo e a política da distribuição. Não use chmod 777
nem execute a bancada como root. Quando existir, `/dev/serial/by-id/` ajuda a escolher
um nome persistente; confira o caminho real antes de passá-lo em `--port`.

## Testes de instalação — sem mover ou abrir a serial

No Windows use `.\.venv\Scripts\python.exe`; no Linux `.venv/bin/python`.
Nos exemplos seguintes, `python` significa esse executável ou o ambiente ativado.

```text
python -m pip check
python -m unittest discover -s tests -v
python buslinker_v2_5.py --help
python buslinker_v3.py --help
python -m serial.tools.list_ports -v
```

A listagem identifica conversores; não confirma alimentação nem comunicação com o servo.
Para verificar a janela gráfica, em uma sessão desktop:

```text
python -m tkinter
python -c "import matplotlib.pyplot as p; p.plot([0,1],[0,1]); p.title('Teste de janela - dados artificiais'); p.show()"
```

Feche as janelas após conferir. No Ubuntu, tkinter depende de python3-tk da versão
de Python utilizada. Em SSH sem display, servidor ou ambiente sem GUI, use `--no-live`
nos movimentos e omita `--live` em monitor/calibrate. CSV e PNG continuam disponíveis.
WSL/VM exigem encaminhamento USB próprio; não presuma que a COM do Windows aparecerá
no Linux convidado. Prefira inicialmente Windows nativo ou Linux nativo.

## Roteiro físico — uma etapa por vez

Leia a [montagem e alimentação](instalacao.md#1-separe-e-conecte-o-material).
Confirme LX-225, placa/revisão, jumpers, fonte 6–8,4 V, limite de corrente, cabos,
percurso mecânico e operador antes de movimentar. Feche outros programas na mesma porta.

Os exemplos abaixo são PowerShell, com COM7 e ID 1 ilustrativos. No Linux, substitua
COM7 pela porta identificada, como `/dev/ttyUSB0`. Para V2.5, substitua o nome do script.

```powershell
python buslinker_v3.py --port COM7 --scan
python tools/diagnose_servo.py --port COM7 --id 1
python buslinker_v3.py monitor --port COM7 --ids 1 --duration 10 --live
```

Esses comandos só consultam. Com leituras válidas e percurso confirmado, faça um
pequeno deslocamento, sem retorno automático:

```powershell
python buslinker_v3.py --port COM7 --ids 1 --move --delta 5 --seconds 2
```

Confira posição inicial/última, alvo, tensão, temperatura e tempo no PNG e nos CSV em
`resultados/<data_hora>/`. A última posição é feedback; não é substituída pelo alvo.
Velocidade é estimada; tempo de coleta não equivale ao tempo de acomodação.

Para dois ou mais servos, configure IDs únicos individualmente, dimensione a fonte,
consulte todos e só então mova. `add-id` não altera o ID físico; veja [change-id](uso.md).

```powershell
python buslinker_v3.py --port COM7 --ids 1 2
python buslinker_v3.py --port COM7 --ids 1 2 --move --delta 5 --seconds 2
```

O movimento padrão começa por comandos em sequência rápida. Para início comum pelo
protocolo, acrescente `--synchronized`: ele dispara por broadcast TODOS os movimentos
pendentes no barramento, inclusive de IDs fora da seleção. Use apenas com estado
conhecido de todo o barramento. Não execute dois programas simultâneos na mesma porta.

`Ctrl+C` tenta interromper/parar o ensaio; falha da comunicação pode impedir STOP.
Parada por software e fechamento da serial não removem torque nem substituem a parada
física prevista na montagem. Interrompa se tensão/temperatura saírem dos limites.

## Evidência a registrar

Registre sistema/versão, arquitetura, Python, versão do kernel ou driver USB, VID/PID,
placa, modelo e IDs, fonte, limite de corrente, carga, comando, commit e pasta dos dados.
Use `python -m pip freeze` para registrar dependências e `git rev-parse HEAD` para o commit.
Dados ausentes: `NOT_MEASURED`. Preserve o CSV original.

TESTADO AUTOMATICAMENTE: testes locais com serial simulada no Windows.
A matriz GitHub Actions verifica Windows e Ubuntu com Python 3.12/3.13; consulte o
resultado de cada execução. Runners não possuem os servos. NÃO TESTADO EM HARDWARE
nesta atualização; compatibilidade física em cada sistema ainda requer ensaio.

## Fontes oficiais

- [WCH CH341SER](https://www.wch.cn/downloads/ch341ser_exe.html): pacote Windows para CH340/CH341.
- [Kernel Linux: ch341](https://github.com/torvalds/linux/blob/master/drivers/usb/serial/ch341.c): implementação do driver serial.
- [pySerial: permissões em Debian](https://pyserial.readthedocs.io/en/latest/appendix.html): grupo dialout e nova sessão.
- [Matplotlib: backends](https://matplotlib.org/stable/users/explain/figure/backends.html): distinção entre janela interativa e renderização sem GUI.
- [Hiwonder BusLinker V3](https://docs.hiwonder.com/projects/BusLinker/en/latest/docs/1_BusLinker_V3.0_Servo_Debugging_Board_User_Manual.html): driver CH341 e modos de comunicação.
