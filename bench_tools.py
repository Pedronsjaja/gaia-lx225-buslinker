"""Monitoramento, cadastro de IDs e ensaios LX-225 para ambas as placas."""
import argparse
import csv
import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path

import serial
from servo_testbench import validate_id, deg_to_ticks, ticks_to_deg

COMMANDS = {'monitor', 'calibrate', 'add-id', 'list-ids', 'change-id', 'offset'}
FIELDS = ['time_s', 'servo_id', 'identifier', 'angle_deg', 'voltage_v',
          'velocity_dps', 'temperature_c', 'target_deg', 'error_deg', 'status']


def load_registry(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Cadastro deve ser um objeto JSON de ID para nome.')
    for key, name in data.items():
        validate_id(int(key))
        if str(int(key)) != key or not isinstance(name, str) or not name.strip():
            raise ValueError('ID ou nome invalido no cadastro.')
    return data


def save_registry(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


class Recorder:
    def __init__(self, folder, live=False):
        import matplotlib
        if not live:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        # A previous headless export or MPLBACKEND=Agg must not silently disable live plots.
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        if live and fig.canvas.required_interactive_framework is None:
            plt.close(fig)
            try:
                plt.switch_backend('TkAgg')
                fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            except (ImportError, RuntimeError) as exc:
                raise ImportError(
                    'Nao foi possivel abrir a janela dos graficos. Instale/ative Tkinter '
                    'no Python utilizado (Linux: python3-tk), ou use --no-live para salvar PNG. '
                    'Teste sem servos: python test_servos.py --plot-test.'
                ) from exc
        self.plt = plt
        self.fig, self.axes = fig, axes
        self.folder = Path(folder) / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.folder.mkdir(parents=True)
        self.file = (self.folder / 'telemetria.csv').open('w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=FIELDS)
        self.writer.writeheader()
        self.rows = []
        self.run_status = "collection"
        self.requested_seconds = math.nan
        self.start = time.monotonic()
        self.live = live
        if live:
            print(f'Graficos ao vivo: backend {matplotlib.get_backend()}; '
                  f'arquivos em {self.folder.resolve()}', flush=True)
            plt.ion()
            plt.show(block=False)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def add(self, state, target=math.nan, status='ok'):
        stamp = state.position_time_s
        row = dict(time_s=stamp-self.start, servo_id=state.servo_id,
                   identifier=state.identifier, angle_deg=state.angle_deg,
                   voltage_v=state.voltage_v, velocity_dps=state.velocity_dps,
                   temperature_c=state.temperature_c, target_deg=target,
                   error_deg=state.angle_deg-target, status=status)
        self.rows.append(row)
        self.writer.writerow(row)
        self.file.flush()

    def failure(self, sid, exc):
        row = dict.fromkeys(FIELDS, math.nan)
        row.update(time_s=time.monotonic()-self.start, servo_id=sid,
                   identifier=f'servo_{sid}', status=str(exc))
        self.rows.append(row)
        self.writer.writerow(row)
        self.file.flush()

    def draw(self):
        metrics = [('angle_deg', 'Posicao (graus)'), ('velocity_dps', 'Velocidade estimada (graus/s)'),
                   ('voltage_v', 'Tensao (V)'), ('temperature_c', 'Temperatura (C)')]
        for ax, (field, title) in zip(self.axes.flat, metrics):
            ax.clear()
            for sid in sorted({r['servo_id'] for r in self.rows}):
                rows = [r for r in self.rows if r['servo_id'] == sid]
                ax.plot([r['time_s'] for r in rows], [r[field] for r in rows], label=f'ID {sid}')
                if field == 'angle_deg' and any(math.isfinite(r['target_deg']) for r in rows):
                    ax.step([r['time_s'] for r in rows], [r['target_deg'] for r in rows],
                            where='post', linestyle='--', label=f'Alvo {sid}')
                valid = [r for r in rows if math.isfinite(r[field])]
                if valid and field != 'velocity_dps':
                    first, last = valid[0], valid[-1]
                    ax.scatter([first['time_s']], [first[field]], marker='o',
                               label=f'Inicial {sid}: {first[field]:.2f}')
                    if len(valid) > 1:
                        ax.scatter([last['time_s']], [last[field]], marker='x',
                                   label=f'Ultima leitura {sid}: {last[field]:.2f}')
            ax.set(xlabel='Tempo desde leitura inicial (s)', ylabel=title)
            ax.grid(True, alpha=0.3)
            if self.rows:
                ax.legend()
        self.fig.tight_layout()
        if self.live:
            self.plt.pause(0.001)

    def save_summary(self):
        summaries = []
        for sid in sorted({r['servo_id'] for r in self.rows}):
            rows = [r for r in self.rows if r['servo_id'] == sid]
            valid = [r for r in rows if math.isfinite(r['angle_deg'])]
            first = valid[0] if valid else {}
            last = valid[-1] if len(valid) > 1 else {}
            row = dict(servo_id=sid, run_status=self.run_status,
                       requested_seconds=self.requested_seconds,
                       initial_time_s=first.get('time_s', math.nan),
                       last_time_s=last.get('time_s', math.nan),
                       observed_duration_s=last.get('time_s', math.nan)-first.get('time_s', math.nan),
                       sample_count=len(valid), failure_count=sum(r['status'] not in ('ok', 'initial', 'simulated') for r in rows))
            for field in ('angle_deg', 'voltage_v', 'temperature_c'):
                row['initial_' + field] = first.get(field, math.nan)
                row['last_' + field] = last.get(field, math.nan)
            row['last_target_deg'] = last.get('target_deg', math.nan)
            row['last_error_deg'] = last.get('error_deg', math.nan)
            summaries.append(row)
        if summaries:
            with (self.folder / 'comparacao.csv').open('w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=list(summaries[0]))
                writer.writeheader()
                writer.writerows(summaries)

    def close(self):
        self.file.close()
        self.save_summary()
        self.draw()
        self.fig.savefig(self.folder / 'graficos.png', dpi=160)
        print(f'CSV e graficos: {self.folder.resolve()}')
        try:
            if self.live:
                print('Graficos salvos. Feche a janela dos graficos para continuar.', flush=True)
                self.plt.show(block=True)
        finally:
            self.plt.close(self.fig)


def plot_demo(output='resultados', live=True):
    """Exercise the real plot pipeline with explicitly simulated data, without serial access."""
    from types import SimpleNamespace
    rec = Recorder(output, live)
    rec.fig.suptitle('SIMULADO - teste dos graficos, sem conexao com servos')
    rec.run_status = 'simulated'
    try:
        for index in range(21):
            t = index / 10
            for sid, direction in ((1, 1), (2, -1)):
                state = SimpleNamespace(servo_id=sid, identifier=f'SIMULATED_{sid}',
                    position_time_s=rec.start + t, angle_deg=100 + direction * 10 * t,
                    voltage_v=7.4, velocity_dps=direction * 10, temperature_c=30)
                rec.add(state, target=100 + direction * 20, status='simulated')
        rec.draw()
    finally:
        rec.close()
    return 0


def check_state(state, max_temp):
    if not 6 <= state.voltage_v <= 8.4:
        raise ValueError(f'ID {state.servo_id}: tensao fora de 6 a 8.4 V.')
    if not math.isfinite(state.temperature_c) or state.temperature_c >= max_temp:
        raise ValueError(f'ID {state.servo_id}: limite de temperatura {max_temp} C.')


def stop_all(bus, ids):
    for sid in ids:
        try:
            bus.stop(sid)
        except (serial.SerialException, OSError) as exc:
            print(f'Nao foi possivel parar ID {sid}: {exc}', file=sys.stderr)


def sample(bus, ids, names, rec, targets=None, max_temp=60, strict=False):
    states = []
    for sid in ids:
        try:
            state = bus.read_servo(sid, names.get(str(sid)))
        except TimeoutError as exc:
            rec.failure(sid, exc)
            print(f'ID {sid}: {exc}', file=sys.stderr)
            if strict:
                raise
            continue
        rec.add(state, (targets or {}).get(sid, math.nan))
        print(f'ID {sid}: {state.angle_deg:.2f} graus | {state.velocity_dps:.2f} graus/s | '
              f'{state.voltage_v:.2f} V | {state.temperature_c:.0f} C')
        if strict:
            check_state(state, max_temp)
        states.append(state)
    if rec.live:
        rec.draw()
    return states


def calibrate(bus, args, ids, names, rec):
    initial = sample(bus, ids, names, rec, max_temp=args.max_temp, strict=True)
    # Prevalida todos os alvos antes de qualquer movimento.
    plans = [{s.servo_id: ticks_to_deg(deg_to_ticks(s.angle_deg + delta))
              for s in initial} for delta in args.deltas]
    # Consultas apenas: nenhum alvo pode ser enviado antes de validar o lote.
    # Os limites internos nao substituem os limites mecanicos da montagem.
    for sid in ids:
        if bus.read_mode(sid) != 0:
            raise ValueError(f'ID {sid}: nao esta em modo de posicao.')
        lower, upper = bus.read_position_limits(sid)
        for targets in plans:
            if not lower <= targets[sid] <= upper:
                raise ValueError(f'ID {sid}: alvo {targets[sid]:.2f} fora dos limites '
                                 f'internos {lower:.2f} a {upper:.2f} graus.')
    results = []
    try:
        for targets in plans:
            bus.move_many([(sid, angle, args.seconds) for sid, angle in targets.items()])
            end = time.monotonic() + args.seconds + args.settle
            while time.monotonic() < end:
                sample(bus, ids, names, rec, targets, args.max_temp, strict=True)
                time.sleep(args.interval)
            samples = []
            for _ in range(args.samples):
                samples.extend(sample(bus, ids, names, rec, targets, args.max_temp, strict=True))
                time.sleep(args.interval)
            for sid in ids:
                values = [s.angle_deg for s in samples if s.servo_id == sid]
                mean = sum(values)/len(values)
                error = mean-targets[sid]
                results.append(dict(servo_id=sid, target_deg=targets[sid], measured_mean_deg=mean,
                                    error_deg=error, spread_deg=max(values)-min(values),
                                    passed=abs(error) <= args.tolerance))
    finally:
        stop_all(bus, ids)
        path = rec.folder / 'calibracao.csv'
        with path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['servo_id', 'target_deg', 'measured_mean_deg',
                                                      'error_deg', 'spread_deg', 'passed'])
            writer.writeheader()
            writer.writerows(results)
    for row in results:
        print(row)
    return 0 if all(r['passed'] for r in results) else 2


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for command in sorted(COMMANDS):
        sp = sub.add_parser(command)
        sp.add_argument('--registry', type=Path, default=Path('servos.json'))
        if command not in ('add-id', 'list-ids'):
            sp.add_argument('--port', required=True)
        if command == 'add-id':
            sp.add_argument('--id', type=int, required=True)
            sp.add_argument('--name', required=True)
        if command == 'change-id':
            sp.add_argument('--from-id', type=int, required=True)
            sp.add_argument('--to-id', type=int, required=True)
            sp.add_argument('--single-servo', action='store_true', required=True,
                            help='Declara que somente o servo a alterar esta conectado')
        if command == 'offset':
            sp.add_argument('--id', type=int, required=True)
            sp.add_argument('--ticks', type=int, help='Offset absoluto -125..125; cada passo = 0.24 grau')
            sp.add_argument('--save', action='store_true', help='Grava o offset na memoria permanente')
        if command in ('monitor', 'calibrate'):
            sp.add_argument('--ids', nargs='+', type=int, help='Omitir para usar todos os IDs cadastrados')
            sp.add_argument('--interval', type=float, default=0.1)
            sp.add_argument('--output', type=Path, default=Path('resultados'))
            sp.add_argument('--live', action='store_true', help='Mostra graficos durante a coleta')
        if command == 'monitor':
            sp.add_argument('--duration', type=float, default=30)
        if command == 'calibrate':
            sp.add_argument('--deltas', nargs='+', type=float, default=[-5, 0, 5, 0],
                            help='Deslocamentos relativos a posicao inicial, em graus')
            sp.add_argument('--seconds', type=float, default=2)
            sp.add_argument('--settle', type=float, default=0.5)
            sp.add_argument('--samples', type=int, default=5)
            sp.add_argument('--tolerance', type=float, default=2)
            sp.add_argument('--max-temp', type=float, default=60)
    return p


def main(bus_class):
    args = parser().parse_args()
    try:
        names = load_registry(args.registry)
        if args.command == 'add-id':
            validate_id(args.id)
            if not args.name.strip():
                raise ValueError('Nome nao pode ser vazio.')
            names[str(args.id)] = args.name.strip()
            save_registry(args.registry, names)
            print(f'ID {args.id} cadastrado como {args.name}. O ID fisico nao foi alterado.')
            return 0
        if args.command == 'list-ids':
            print(json.dumps(names, ensure_ascii=False, indent=2))
            return 0
        if args.command == 'change-id':
            validate_id(args.from_id)
            validate_id(args.to_id)
            if str(args.to_id) in names:
                raise ValueError('ID de destino ja cadastrado; escolha outro ID.')
            with bus_class(args.port) as bus:
                bus.write_id(args.from_id, args.to_id)
            print(f'ID fisico confirmado: {args.to_id}')
            names[str(args.to_id)] = names.pop(str(args.from_id), f'servo_{args.to_id}')
            save_registry(args.registry, names)
            return 0
        if args.command == 'offset':
            validate_id(args.id)
            if args.save and args.ticks is None:
                raise ValueError('--save exige --ticks explicito.')
            if args.ticks is not None and not -125 <= args.ticks <= 125:
                raise ValueError('Ticks devem estar entre -125 e 125.')
            with bus_class(args.port) as bus:
                old = bus.read_offset(args.id)
                print(f'Offset anterior: {old} ticks ({old*0.24:.2f} graus). Anote para restaurar.')
                if args.ticks is not None:
                    print('Aplicando offset absoluto; o eixo pode se mover.')
                    bus.set_offset(args.id, args.ticks, save=args.save)
                    print(f'Offset confirmado: {args.ticks}. Gravacao permanente solicitada: {args.save}.')
            return 0
        ids = args.ids if args.ids is not None else [int(k) for k in names]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError('Informe IDs unicos ou cadastre-os com add-id.')
        for sid in ids:
            validate_id(sid)
        if not math.isfinite(args.interval) or args.interval < 0.01:
            raise ValueError('Intervalo deve ser finito e >= 0.01 s.')
        if args.command == 'monitor':
            if not math.isfinite(args.duration) or args.duration <= 0:
                raise ValueError('Duracao deve ser finita e positiva.')
        else:
            for value, low, high in [(args.seconds, 0.5, 30), (args.settle, 0, 30),
                                     (args.tolerance, 0, 240), (args.max_temp, 1, 85)]:
                if not math.isfinite(value) or not low <= value <= high:
                    raise ValueError('Tempo, tolerancia ou temperatura fora dos limites.')
            if not 1 <= args.samples <= 100:
                raise ValueError('Use 1 a 100 amostras.')
            if any(not math.isfinite(v) or abs(v) > 10 for v in args.deltas):
                raise ValueError('Cada delta deve estar entre -10 e 10 graus.')
        rec = Recorder(args.output, args.live)
        try:
            with bus_class(args.port) as bus:
                if args.command == 'calibrate':
                    return calibrate(bus, args, ids, names, rec)
                end = time.monotonic() + args.duration
                while time.monotonic() < end:
                    sample(bus, ids, names, rec)
                    time.sleep(args.interval)
                return 0 if rec.rows and all(r['status'] == 'ok' for r in rec.rows) else 1
        finally:
            rec.close()
    except (ValueError, TimeoutError, serial.SerialException, OSError, ImportError) as exc:
        print(f'Falha: {exc}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('Interrompido. Dados coletados foram preservados.', file=sys.stderr)
        return 130
