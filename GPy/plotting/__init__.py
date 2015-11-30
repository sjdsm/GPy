# Copyright (c) 2014, GPy authors (see AUTHORS.txt).
# Licensed under the BSD 3-clause license (see LICENSE.txt)
from ConfigParser import NoOptionError

current_lib = [None]

supported_libraries = ['matplotlib', 'plotly', 'none']
error_suggestion = "Please make sure you specify your plotting library in your configuration file.\n\n[plotting]\nlibrary = <library>\n\nCurrently supported libraries: {}".format(", ".join(supported_libraries))

def change_plotting_library(lib):
    try:
        #===========================================================================
        # Load in your plotting library here and
        # save it under the name plotting_library!
        # This is hooking the library in
        # for the usage in GPy:
        if lib not in supported_libraries:
            raise NoOptionError("Warning: Plotting library {} not recognized, currently supported libraries are: \n {}".format(lib, ", ".join(supported_libraries)))
        if lib == 'matplotlib':
            import matplotlib
            from .matplot_dep.plot_definitions import MatplotlibPlots
            from .matplot_dep import visualize, mapping_plots, priors_plots, ssgplvm, svig_plots, variational_plots, img_plots
            current_lib[0] = MatplotlibPlots()
        if lib == 'plotly':
            import plotly
            from .plotly_dep.plot_definitions import PlotlyPlots
            current_lib[0] = PlotlyPlots()
        if lib == 'none':
            current_lib[0] = None
        #===========================================================================
    except (ImportError, NameError):
        config.set('plotting', 'library', 'none')
        import warnings
        warnings.warn(ImportWarning("{} not available, install newest version of {} for plotting".format(lib, lib)))

from ..util.config import config
try:
    lib = config.get('plotting', 'library')
    change_plotting_library(lib)
except NoOptionError:
    print("No plotting library was specified. \n{}".format(error_suggestion))


def plotting_library():
    if current_lib[0] is None:
        raise RuntimeError("No plotting library was loaded. \n{}".format(error_suggestion))
    return current_lib[0]

def show(figure, **kwargs):
    """
    Show the specific plotting library figure, returned by
    add_to_canvas().

    kwargs are the plotting library specific options
    for showing/drawing a figure.
    """
    return plotting_library().show_canvas(figure, **kwargs)

if config.get('plotting', 'library') is not 'none':
    # Inject the plots into classes here:

    # Already converted to new style:
    from . import gpy_plot

    from ..core import GP
    GP.plot_data = gpy_plot.data_plots.plot_data
    GP.plot_data_error = gpy_plot.data_plots.plot_data_error
    GP.plot_errorbars_trainset = gpy_plot.data_plots.plot_errorbars_trainset
    GP.plot_mean = gpy_plot.gp_plots.plot_mean
    GP.plot_confidence = gpy_plot.gp_plots.plot_confidence
    GP.plot_density = gpy_plot.gp_plots.plot_density
    GP.plot_samples = gpy_plot.gp_plots.plot_samples
    GP.plot = gpy_plot.gp_plots.plot
    GP.plot_f = gpy_plot.gp_plots.plot_f
    GP.plot_magnification = gpy_plot.latent_plots.plot_magnification

    from ..core import SparseGP
    SparseGP.plot_inducing = gpy_plot.data_plots.plot_inducing

    from ..models import GPLVM, BayesianGPLVM, bayesian_gplvm_minibatch, SSGPLVM, SSMRD
    GPLVM.plot_latent = gpy_plot.latent_plots.plot_latent
    GPLVM.plot_scatter = gpy_plot.latent_plots.plot_latent_scatter
    GPLVM.plot_inducing = gpy_plot.latent_plots.plot_latent_inducing
    GPLVM.plot_steepest_gradient_map = gpy_plot.latent_plots.plot_steepest_gradient_map
    BayesianGPLVM.plot_latent = gpy_plot.latent_plots.plot_latent
    BayesianGPLVM.plot_scatter = gpy_plot.latent_plots.plot_latent_scatter
    BayesianGPLVM.plot_inducing = gpy_plot.latent_plots.plot_latent_inducing
    BayesianGPLVM.plot_steepest_gradient_map = gpy_plot.latent_plots.plot_steepest_gradient_map
    bayesian_gplvm_minibatch.BayesianGPLVMMiniBatch.plot_latent = gpy_plot.latent_plots.plot_latent
    bayesian_gplvm_minibatch.BayesianGPLVMMiniBatch.plot_scatter = gpy_plot.latent_plots.plot_latent_scatter
    bayesian_gplvm_minibatch.BayesianGPLVMMiniBatch.plot_inducing = gpy_plot.latent_plots.plot_latent_inducing
    bayesian_gplvm_minibatch.BayesianGPLVMMiniBatch.plot_steepest_gradient_map = gpy_plot.latent_plots.plot_steepest_gradient_map
    SSGPLVM.plot_latent = gpy_plot.latent_plots.plot_latent
    SSGPLVM.plot_scatter = gpy_plot.latent_plots.plot_latent_scatter
    SSGPLVM.plot_inducing = gpy_plot.latent_plots.plot_latent_inducing
    SSGPLVM.plot_steepest_gradient_map = gpy_plot.latent_plots.plot_steepest_gradient_map

    from ..kern import Kern
    Kern.plot_covariance = gpy_plot.kernel_plots.plot_covariance
    def deprecate_plot(self, *args, **kwargs):
        import warnings
        warnings.warn(DeprecationWarning('Kern.plot is being deprecated and will not be available in the 1.0 release. Use Kern.plot_covariance instead'))
        return self.plot_covariance(*args, **kwargs)
    Kern.plot = deprecate_plot
    Kern.plot_ARD = gpy_plot.kernel_plots.plot_ARD

    from ..inference.optimization import Optimizer
    Optimizer.plot = gpy_plot.inference_plots.plot_optimizer
    # Variational plot!
