"""Test real Tk windows with SIMULATED samples, without serial access.

Run: python tools/check_plot_window.py (requires desktop and Tkinter).
Opens and automatically closes a window for each program variant.
"""
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
import bench_tools
import buslinker_v2_5
import buslinker_v3


def main():
    for module in (bench_tools, buslinker_v2_5, buslinker_v3):
        matplotlib.use('Agg')  # Reproduce a file-only backend left by an export.
        with tempfile.TemporaryDirectory() as tmp:
            rec = module.Recorder(tmp, live=True)
            rec.run_status = 'simulated'
            rec.fig.suptitle('SIMULADO - teste automatico da janela, sem servos')
            for index in range(11):
                for sid in (1, 2):
                    rec.add(SimpleNamespace(servo_id=sid, identifier=f'SIMULATED_{sid}',
                        position_time_s=rec.start + index / 10,
                        angle_deg=90 + sid * index, velocity_dps=sid * 10,
                        voltage_v=7.4, temperature_c=30),
                        target=90 + sid * 10, status='simulated')
            rec.draw()
            assert len(rec.fig.axes) == 4
            assert all(len(ax.lines) >= 2 for ax in rec.axes.flat)
            window = rec.fig.canvas.manager.window
            window.update()
            assert window.winfo_viewable(), 'Janela nao visivel'
            observed = []

            def verify_and_close():
                observed.append(window.winfo_viewable())
                rec.plt.close(rec.fig)

            window.after(1000, verify_and_close)
            rec.close()
            assert observed == [1], observed
            assert (rec.folder / 'graficos.png').stat().st_size > 1000
            print('GUI_OK', module.__name__, matplotlib.get_backend(),
                  '4 paineis, 2 IDs simulados, janela visivel e eventos processados')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
