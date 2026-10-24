<div align="center">

<h1>⚙️ Gaia &#183; LX-225 / BusLinker</h1>
<p><strong>Da conex&#227;o do primeiro servo &#224; bancada de diagn&#243;stico e calibra&#231;&#227;o.</strong></p>
<p><kbd>Python &#183; LX-225 &#183; BusLinker V2.5 / V3</kbd></p>

<p><a href="https://github.com/Pedronsjaja/gaia-lx225-buslinker/stargazers"><img alt="Estrelas no GitHub" src="https://img.shields.io/github/stars/Pedronsjaja/gaia-lx225-buslinker?style=flat-square&amp;color=147d68"/></a> <a href="https://github.com/Pedronsjaja/gaia-lx225-buslinker/commits/main"><img alt="Último commit" src="https://img.shields.io/github/last-commit/Pedronsjaja/gaia-lx225-buslinker?style=flat-square&amp;color=235789"/></a></p>
<p><a href="#inicio-rapido">Comece aqui</a> · <a href="#guia-do-projeto">Documentação</a> · <a href="https://github.com/Pedronsjaja/gaia-lx225-buslinker/tree/main">Arquivos</a></p>

</div>

<a id="inicio-rapido"></a>
## 🚀 Comece aqui

**[Instalar e fazer o primeiro teste](docs/instalacao.md)**

| Comunicação | Bancada | Documentação |
| --- | --- | --- |
| Biblioteca e programas para cada revisão da placa. | Posição, tensão, temperatura e movimentos de teste. | Manuais, alimentação, IDs e solução de problemas. |

### Caminho do projeto

```mermaid
flowchart LR
  N0["Conferir placa"]
  N1["Instalar dependências"]
  N0 --> N1
  N2["Consultar estado"]
  N1 --> N2
  N3["Testar movimento"]
  N2 --> N3
```

<a id="guia-do-projeto"></a>
## 📖 Documentação

Bancada e biblioteca Python para o **servo Hiwonder LX-225** com **BusLinker V2.5 ou V3**: comunicação, consulta de posição/tensão/temperatura, movimentos de teste, gráficos, IDs e calibração.

## Comece aqui

1. Leia [como usar o GitHub](docs/primeiros-passos-github.md), se esta for sua primeira visita.
2. Siga a [instalação e primeiro teste](docs/instalacao.md), começando com um único servo.
3. Confira os [manuais e esquemas](docs/datasheets/README.md) da sua placa.
4. Use o [manual de comandos](docs/uso.md) e registre os resultados da bancada.

| Quero… | Abrir |
| --- | --- |
| Instalar Python, ligar a placa e identificar a porta | [Instalação](docs/instalacao.md) |
| Manuais V2.5/V3 e ficha LX-225 | [Documentação técnica](docs/datasheets/README.md) |
| Software Hiwonder e driver USB | [Softwares e drivers](docs/softwares-e-drivers.md) |
| Consultar sensores, mover ou calibrar | [Comandos Python](docs/uso.md) |
| Resolver erros | [Solução de problemas](docs/solucao-de-problemas.md) |
| Conferir alimentação e barramento | [Eletrônica do LX-225](docs/eletronica/README.md) |
| Reutilizar a biblioteca no robô | [Interface dos atuadores](docs/gaia_lx225.md) |
| Baixar CAD do servo e suportes | [Catálogo no repositório de estrutura](https://github.com/Pedronsjaja/gaia-humanoid-structure/blob/main/hardware/README.md) |

## Qual programa usar?

Para conferir os quatro gráficos **sem conectar ou mover servos**, execute:

```powershell
python test_servos.py --plot-test
```

A janela usa dados marcados como **SIMULADOS** e permanece aberta até ser fechada.
O mesmo argumento funciona em `buslinker_v2_5.py` e `buslinker_v3.py`.
Nos movimentos do menu (`--interactive`, opções 2 e 4), os gráficos usam o
feedback dos servos. A opção 4 permite uma posição absoluta diferente por ID.
O programa imprime seu caminho ao iniciar, para identificar cópias antigas.

| Placa | Programa independente | Classe |
| --- | --- | --- |
| BusLinker V2.5 | [buslinker_v2_5.py](buslinker_v2_5.py) | `BusLinkerV2_5` |
| BusLinker V3 | [buslinker_v3.py](buslinker_v3.py) | `BusLinkerV3` |

Instale as dependências de [requirements.txt](requirements.txt). Os dois programas usam o protocolo LX-225 a 115200 baud. Confira o comando da sua revisão no tutorial; V3 não significa compatibilidade com qualquer protocolo de servo.

Comece consultando o estado. Antes de mover, confirme ID, alimentação, limites e percurso mecânico. A referência elétrica e as diferenças entre tensão da placa e do servo estão nos [manuais](docs/datasheets/README.md).

## Organização

```text
buslinker_v2_5.py       Programa completo V2.5
buslinker_v3.py         Programa completo V3
servo_testbench.py     Comunicação compartilhada
bench_tools.py         Gráficos, IDs e calibração
test_servos.py         Interface da bancada
docs/                  Instalação, uso, manuais e diagnóstico
tests/                 Testes com serial simulada
tools/                 Diagnóstico e geração dos programas
```

Para desenvolver, altere as fontes compartilhadas e gere novamente os programas independentes com `python tools/build_standalone.py`.

```powershell
python -m unittest discover -s tests -v
```

Os testes de software não certificam a montagem elétrica ou mecânica. Corrente e torque não são medidos por este driver; a velocidade exibida é estimada entre leituras.

## Repositórios da equipe Gaia

| Preciso de… | Repositório |
| --- | --- |
| Servo LX-225, BusLinker, drivers e testes de bancada | [LX-225 / BusLinker](https://github.com/Pedronsjaja/gaia-lx225-buslinker) |
| Gazebo, OP3, ROS 2 e autonomia | [Simulação](https://github.com/Pedronsjaja/gaia-humanoid-simulation) |
| CAD, suportes, montagem e requisitos físicos da CBR | [Estrutura](https://github.com/Pedronsjaja/gaia-humanoid-structure) |
| Instalar Ubuntu 24.04 e ROS 2 Jazzy | [Ambiente Linux / ROS 2](https://github.com/Pedronsjaja/gaia-ros2-ubuntu24) |

Cada repositório tem seus próprios arquivos, Issues e histórico. Abra dúvidas na área correspondente; inclua links quando uma mudança depender de outra área.

O antigo repositório `gaia-humanoid-robot` foi renomeado para este endereço. Simulação e arquivos mecânicos passaram para os repositórios acima; o histórico anterior permanece preservado.


## Windows 10/11 e Linux

Consulte o [guia de instalação e testes por sistema](docs/windows-linux.md): drivers USB, Ubuntu/Debian/Mint/Pop!_OS, ambiente Python, gráficos e ensaios com um ou vários servos.

## Aula de Python, ROS 2 e servos

Leia [Da câmera aos servos — guia ilustrado da equipe Gaia](https://github.com/Pedronsjaja/gaia-humanoid-simulation/blob/2db129f822519ea28f9817e6f49a3da896ee8ce6/docs/programacao/da-camera-aos-servos.md) (revisão fixa). Entenda o que o driver Python já faz, o significado de tópicos/services/actions e como nomes e radianos se relacionam com IDs e graus. A arquitetura da ponte ROS/LX-225 continua a definir. A tomada de decisão/autonomia permanece pendente. O material reúne diagramas, ilustração conceitual, exercícios e referências; não implementa controle físico.
