import os

import numpy as np

from PySDM.backends import CPU
from PySDM.builder import Builder
from PySDM.environments import Box
from PySDM.dynamics import Coalescence
from PySDM.initialisation.spectral_sampling import ConstantMultiplicity

from PySDM_examples.Shima_et_al_2009.settings import Settings
from PySDM_examples.Shima_et_al_2009.spectrum_plotter import SpectrumPlotter
from PySDM.products.state import ParticlesVolumeSpectrum
from PySDM.products.stats.timers import WallTime


def run(settings, backend=CPU, observers=()):
    builder = Builder(n_sd=settings.n_sd, backend=backend(formulae=settings.formulae))
    builder.set_environment(Box(dv=settings.dv, dt=settings.dt))
    attributes = {}
    attributes['volume'], attributes['n'] = ConstantMultiplicity(settings.spectrum).sample(settings.n_sd)
    coalescence = Coalescence(settings.kernel, adaptive=settings.adaptive)
    builder.add_dynamic(coalescence)
    products = [ParticlesVolumeSpectrum(settings.radius_bins_edges), WallTime()]
    particulator = builder.build(attributes, products)
    if hasattr(settings, 'u_term') and 'terminal velocity' in particulator.particles.attributes:
        particulator.particles.attributes['terminal velocity'].approximation = settings.u_term(particulator)

    for observer in observers:
        particulator.observers.append(observer)

    vals = {}
    particulator.products['wall_time'].reset()
    for step in settings.output_steps:
        particulator.run(step - particulator.n_steps)
        vals[step] = particulator.products['dv/dlnr'].get()[0]
        vals[step][:] *= settings.rho

    exec_time = particulator.products['wall_time'].get()
    return vals, exec_time


def main(plot: bool, save: str):
    with np.errstate(all='raise'):
        settings = Settings()

        settings.n_sd = 2 ** 15

        states, _ = run(settings)

    with np.errstate(invalid='ignore'):
        plotter = SpectrumPlotter(settings)
        plotter.smooth = True
        for step, vals in states.items():
            error = plotter.plot(vals, step * settings.dt)
            #assert error < 200  # TODO #327
        if save is not None:
            n_sd = settings.n_sd
            plotter.save(save + "/" +
                         f"{n_sd}_shima_fig_2" +
                         "." + plotter.format)
        if plot:
            plotter.show()


if __name__ == '__main__':
    main(plot='CI' not in os.environ, save=None)
