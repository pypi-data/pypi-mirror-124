import numpy as np
import pytest

from PySDM.environments import Box
from PySDM.initialisation.spatial_sampling import Pseudorandom
from PySDM.state.mesh import Mesh
from PySDM.dynamics.coalescence import default_dt_coal_range
# noinspection PyUnresolvedReferences
from ....backends_fixture import backend
from .__parametrisation__ import get_dummy_particulator_and_sdm


class TestSDMMultiCell:

    @staticmethod
    @pytest.mark.parametrize("n_sd", [2, 3, 8000])
    @pytest.mark.parametrize("adaptive", [False, True])
    def test_coalescence_call(n_sd, backend, adaptive):
        # TODO #330
        from PySDM.backends import ThrustRTC
        if backend is ThrustRTC:
            return

        # Arrange
        n = np.ones(n_sd)
        v = np.ones_like(n)
        env = Box(dv=1, dt=default_dt_coal_range[1])
        grid = (25, 25)
        env.mesh = Mesh(grid, size=grid)
        particulator, sut = get_dummy_particulator_and_sdm(backend, len(n), environment=env)
        cell_id, _, _ = env.mesh.cellular_attributes(Pseudorandom.sample(grid, len(n)))
        attributes = {'n': n, 'volume': v, 'cell id': cell_id}
        particulator.build(attributes)
        u01, _ = sut.rnd_opt.get_random_arrays()
        sut.actual_length = particulator.attributes._Particles__idx.length
        sut.adaptive = adaptive

        # Act
        sut()

        # Assert
        np.testing.assert_array_equal(cell_id, particulator.attributes['cell id'].to_ndarray(raw=True))
