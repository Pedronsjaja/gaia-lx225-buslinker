import csv
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import bench_tools as b
import test_servos as cli
from servo_testbench import ServoState, LX225Bus


class RecordingTests(unittest.TestCase):
    def state(self, angle=120, stamp=10, temp=30):
        return ServoState(1, 'servo_1', angle, 7.4, 0, temperature_c=temp, position_time_s=stamp)

    def bus(self):
        bus = MagicMock()
        bus._move_params.side_effect = LX225Bus._move_params
        bus.read_mode.return_value = 0
        bus.read_position_limits.return_value = (0, 240)
        bus.read_servo.return_value = self.state(125, 13)
        return bus

    def test_completed_movement_exports_measured_endpoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            bus = self.bus()
            with patch.object(cli.time, 'monotonic', side_effect=[10, 10, 14]):
                cli.recorded_movement(bus, [self.state()], 5, 2, output=tmp, live=False)
            folder = next(Path(tmp).iterdir())
            with (folder / 'comparacao.csv').open() as f:
                row = next(csv.DictReader(f))
            self.assertEqual(row['run_status'], 'completed')
            self.assertEqual(float(row['initial_angle_deg']), 120)
            self.assertEqual(float(row['last_angle_deg']), 125)
            self.assertEqual(float(row['observed_duration_s']), 3)
            self.assertAlmostEqual(float(row['last_target_deg']), 125.04)
            self.assertGreater((folder / 'graficos.png').stat().st_size, 1000)
            bus.stop.assert_called_once_with(1)

    def test_missing_final_sample_is_not_initial_position(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = b.Recorder(tmp)
            rec.add(self.state(), status='initial')
            rec.run_status = 'interrupted'
            rec.failure(1, TimeoutError('sem resposta'))
            rec.close()
            with (rec.folder / 'comparacao.csv').open() as f:
                row = next(csv.DictReader(f))
            self.assertTrue(math.isnan(float(row['last_angle_deg'])))
            self.assertEqual(row['failure_count'], '1')

    def test_timeout_preserves_csv_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            bus = self.bus()
            bus.read_servo.side_effect = TimeoutError('sem resposta')
            with patch.object(cli.time, 'monotonic', side_effect=[10, 10, 14, 14]):
                with self.assertRaises(TimeoutError):
                    cli.recorded_movement(bus, [self.state()], 5, 2, output=tmp, live=False)
            folder = next(Path(tmp).iterdir())
            with (folder / 'comparacao.csv').open() as f:
                row = next(csv.DictReader(f))
            self.assertEqual(row['run_status'], 'interrupted')
            self.assertEqual(row['failure_count'], '1')
            bus.stop.assert_called_once_with(1)

    def test_hot_or_unknown_temperature_prevents_motion(self):
        for temp in (60, math.nan):
            bus = self.bus()
            with self.assertRaises(ValueError):
                cli.test_movement(bus, [self.state(temp=temp)], 5, 2)
            bus.move_verified.assert_not_called()

    def test_individual_targets_export_per_servo(self):
        states = [self.state(), ServoState(2, 'servo_2', 120, 7.4, 0,
                  temperature_c=30, position_time_s=10)]
        with tempfile.TemporaryDirectory() as tmp:
            bus = self.bus()
            bus.read_servo.side_effect = lambda sid: ServoState(
                sid, f'servo_{sid}', {1: 90, 2: 140}[sid], 7.4, 0,
                temperature_c=30, position_time_s=13)
            with patch.object(cli.time, 'monotonic', side_effect=[10, 10, 14]):
                cli.recorded_movement(bus, states, 0, 2, output=tmp, live=False,
                                      target_angles={1: 90, 2: 140})
            bus.move_group_direct.assert_called_once_with([(1, 90, 2), (2, 140, 2)])
            folder = next(Path(tmp).iterdir())
            with (folder / 'comparacao.csv').open() as f:
                rows = {int(row['servo_id']): row for row in csv.DictReader(f)}
            for sid, target in ((1, 90), (2, 140)):
                self.assertAlmostEqual(float(rows[sid]['last_target_deg']), round(target / 0.24) * 0.24)
            self.assertGreater((folder / 'graficos.png').stat().st_size, 1000)

    def test_invalid_individual_target_blocks_entire_group(self):
        states = [self.state(), ServoState(2, 'servo_2', 120, 7.4, 0,
                  temperature_c=30, position_time_s=10)]
        for targets in ({1: 90}, {1: 90, 2: float('nan')},
                        {1: 90, 2: 230}, {1: 90, 2: 190}, {1: 90, 2: -1}):
            with self.subTest(targets=targets):
                bus = self.bus()
                bus.read_torque_enabled.return_value = False
                bus.read_position_limits.return_value = (0, 180)
                with self.assertRaises(ValueError):
                    cli.test_movement(bus, states, 0, 2, target_angles=targets)
                bus.move_verified.assert_not_called()
                bus.move_group_direct.assert_not_called()
                bus.move_many_verified.assert_not_called()
