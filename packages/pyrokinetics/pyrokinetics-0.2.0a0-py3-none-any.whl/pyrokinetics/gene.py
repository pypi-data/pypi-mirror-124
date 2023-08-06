import f90nml
import copy

import numpy as np

from .constants import deuterium_mass, electron_charge, electron_mass, pi
from .local_species import LocalSpecies
from .numerics import Numerics
from .gk_code import GKCode
from .gk_output import GKOutput
import os
from path import Path
from cleverdict import CleverDict


class GENE(GKCode):
    """
    Basic GENE object

    """

    def __init__(self):

        self.base_template_file = os.path.join(
            Path(__file__).dirname(), "templates", "input.gene"
        )
        self.default_file_name = "input.gene"

    def read(self, pyro, data_file=None, template=False):
        """
        Reads a GENE input file and loads pyro object with the data
        """

        if template and data_file is None:
            data_file = self.base_template_file

        gene = f90nml.read(data_file).todict()

        pyro.initial_datafile = copy.copy(gene)

        try:
            nl_flag = gene["general"]["nonlinear"]

            if nl_flag == ".F.":

                pyro.linear = True
            else:
                pyro.linear = False
        except KeyError:
            pyro.linear = True

        pyro.gene_input = gene

        # Loads pyro object with equilibrium data
        if not template:
            self.load_pyro(pyro)

        # Load Pyro with numerics if they don't exist
        if not hasattr(pyro, "numerics"):
            self.load_numerics(pyro, gene)

    def load_pyro(self, pyro):
        """
        Loads LocalSpecies, LocalGeometry, Numerics classes from pyro.gene_input
        """

        # Geometry
        gene = pyro.gene_input

        gene_eq = gene["geometry"]["magn_geometry"]

        if gene_eq == "s_alpha":
            pyro.local_geometry = "SAlpha"
        elif gene_eq == "miller":
            pyro.local_geometry = "Miller"

        #  Load GENE with local geometry
        self.load_local_geometry(pyro, gene)

        # Load GENE with species data
        self.load_local_species(pyro, gene)

        # Need species to set up beta_prime

        if pyro.local_geometry_type == "Miller":
            if pyro.local_geometry.B0 is not None:
                pyro.local_geometry.beta_prime = (
                    -pyro.local_species.a_lp / pyro.local_geometry.B0 ** 2
                )
            else:
                pyro.local_geometry.beta_prime = 0.0
        else:
            raise NotImplementedError

        # Load Pyro with numerics
        self.load_numerics(pyro, gene)

    def write(self, pyro, filename, directory="."):
        """
        Write a GENE input file from a pyro object

        """

        if not os.path.exists(directory):
            os.makedirs(directory)

        path_to_file = os.path.join(directory, filename)

        gene_input = pyro.gene_input

        # Geometry data
        if pyro.local_geometry_type == "Miller":
            miller = pyro.local_geometry

            # Ensure Miller settings in input file
            gene_input["geometry"]["magn_geometry"] = "miller"

            # Reference B field
            bref = miller.B0

            # Assign Miller values to input file
            pyro_gene_miller = self.pyro_to_code_miller()

            # GENE uses definitions consistent with Miller.
            for key, val in pyro_gene_miller.items():
                gene_input[val[0]][val[1]] = miller[key]

        else:
            raise NotImplementedError(
                f"Writing {pyro.geometry_type} for GENE not supported yet"
            )

        # gene_input['general']['coll'] = (4*(deuterium_mass/electron_mass)**0.5)*local_species.electron.nu
        gene_input["geometry"]["amhd"] = (
            -(miller.q ** 2) * miller.Rmaj * miller.beta_prime
        )
        gene_input["geometry"]["trpeps"] = miller.rho / miller.Rmaj

        # Kinetic data
        local_species = pyro.local_species
        gene_input["box"]["n_spec"] = local_species.nspec

        pyro_gene_species = self.pyro_to_code_species()

        for iSp, name in enumerate(local_species.names):

            species_key = "species"

            if name == "electron":
                gene_input[species_key][iSp]["name"] = "electron"
            else:
                try:
                    gene_input[species_key][iSp]["name"] = "ion"
                except IndexError:
                    gene_input[species_key].append(
                        copy.copy(gene_input[species_key][0])
                    )
                    gene_input[species_key][iSp]["name"] = "ion"

            for key, val in pyro_gene_species.items():
                gene_input[species_key][iSp][val] = local_species[name][key]

        # If species are defined calculate beta
        if local_species.nref is not None:

            pref = local_species.nref * local_species.tref * electron_charge

            beta = pref / bref ** 2 * 8 * pi * 1e-7

        # Calculate from reference  at centre of flux surface
        else:
            if pyro.local_geometry_type == "Miller":
                if miller.B0 is not None:
                    beta = 1 / miller.B0 ** 2 * (miller.Rgeo / miller.Rmaj) ** 2
                else:
                    beta = 0.0
            else:
                raise NotImplementedError

        gene_input["general"]["beta"] = beta

        gene_input["general"]["coll"] = (
            (4 * (deuterium_mass / electron_mass) ** 0.5) ** -1
        ) * local_species.electron.nu

        # Numerics
        numerics = pyro.numerics

        if numerics.bpar and not numerics.apar:
            raise ValueError("Can't have bpar without apar in GENE")

        gene_input["general"]["bpar"] = numerics.bpar

        if not numerics.apar:
            gene_input["general"]["beta"] = 0.0

        gene_input["general"]["dt_max"] = numerics.delta_time
        gene_input["general"]["simtimelim"] = numerics.max_time

        if numerics["nonlinear"]:

            gene_input["general"]["nonlinear"] = True
            gene_input["box"]["nky0"] = numerics["nky"]
            gene_input["box"]["nkx"] = numerics["nkx"]

        else:
            gene_input["general"]["nonlinear"] = False

        gene_input["box"]["nky0"] = numerics.nky
        gene_input["box"]["kymin"] = numerics.ky

        if numerics.kx != 0.0:
            gene_input["box"]["lx"] = 2 * pi / numerics.kx

        gene_input["box"]["nz0"] = numerics.ntheta
        gene_input["box"]["nv0"] = 2 * numerics.nenergy
        gene_input["box"]["nw0"] = numerics.npitch

        # Currently forces NL sims to have nperiod = 1
        gene_nml = f90nml.Namelist(gene_input)
        gene_nml.float_format = pyro.float_format
        gene_nml.write(path_to_file, force=True)

    def load_local_geometry(self, pyro, gene):
        """
        Loads LocalGeometry class from pyro.gene_input
        """

        if pyro.local_geometry_type == "Miller":
            self.load_miller(pyro, gene)

    def load_miller(self, pyro, gene):
        """
        Load Miller class from pyro.gene_input
        """

        # Set some defaults here
        gene["geometry"]["magn_geometry"] = "miller"

        pyro_gene_miller = self.pyro_to_code_miller()

        miller = pyro.local_geometry

        for key, val in pyro_gene_miller.items():
            miller[key] = gene[val[0]][val[1]]

        miller.kappri = miller.s_kappa * miller.kappa / miller.rho
        miller.tri = np.arcsin(miller.delta)

        # Get beta normalised to R_major(in case R_geo != R_major)
        beta = gene["general"]["beta"] * (miller.Rmaj / miller.Rgeo) ** 2

        # Can only know Bunit/B0 from local Miller
        miller.bunit_over_b0 = miller.get_bunit_over_b0()

        # Assume pref*8pi*1e-7 = 1.0
        if beta != 0.0:
            miller.B0 = np.sqrt(1.0 / beta)
        else:
            # If beta = 0
            miller.B0 = None

        pyro.miller = miller

    def load_local_species(self, pyro, gene):
        """
        Load LocalSpecies object from pyro.gene_input
        """

        nspec = gene["box"]["n_spec"]
        pyro_gene_species = self.pyro_to_code_species()

        # Dictionary of local species parameters
        local_species = LocalSpecies()
        local_species["nspec"] = nspec
        local_species["nref"] = None
        local_species["names"] = []

        ion_count = 0

        gene_nu_ei = gene["general"]["coll"]

        # Load each species into a dictionary
        for i_sp in range(nspec):

            species_data = CleverDict()

            gene_key = "species"

            gene_data = gene[gene_key][i_sp]

            for pyro_key, gene_key in pyro_gene_species.items():
                species_data[pyro_key] = gene_data[gene_key]

            species_data["vel"] = 0.0
            species_data["a_lv"] = 0.0

            if species_data.z == -1:
                name = "electron"
                te = species_data.temp
                ne = species_data.dens
                me = species_data.mass

                species_data.nu = (
                    gene_nu_ei * 4 * (deuterium_mass / electron_mass) ** 0.5
                )

            else:
                ion_count += 1
                name = f"ion{ion_count}"
                species_data.nu = None

            species_data.name = name

            # Add individual species data to dictionary of species
            local_species.add_species(name=name, species_data=species_data)

        # Normalise to pyrokinetics normalisations and calculate total pressure gradient
        for name in local_species.names:
            species_data = local_species[name]

            species_data.temp = species_data.temp / te
            species_data.dens = species_data.dens / ne

        nu_ee = local_species.electron.nu

        for ion in range(ion_count):
            key = f"ion{ion + 1}"

            nion = local_species[key]["dens"]
            tion = local_species[key]["temp"]
            mion = local_species[key]["mass"]
            # Not exact at log(Lambda) does change but pretty close...
            local_species[key]["nu"] = (
                nu_ee
                * (nion / tion ** 1.5 / mion ** 0.5)
                / (ne / te ** 1.5 / me ** 0.5)
            )

        # Add local_species
        pyro.local_species = local_species

    def pyro_to_code_miller(self):
        """
        Generates dictionary of equivalent pyro and gene parameter names
        for miller parameters
        """

        pyro_gene_param = {
            "rho": ["geometry", "minor_r"],
            "Rmaj": ["geometry", "major_r"],
            "Rgeo": ["geometry", "major_r"],
            "q": ["geometry", "q0"],
            "kappa": ["geometry", "kappa"],
            "s_kappa": ["geometry", "s_kappa"],
            "delta": ["geometry", "delta"],
            "s_delta": ["geometry", "s_delta"],
            "shat": ["geometry", "shat"],
            "shift": ["geometry", "drr"],
        }

        return pyro_gene_param

    def pyro_to_code_species(self):
        """
        Generates dictionary of equivalent pyro and gene parameter names
        for species parameters
        """

        pyro_gene_species = {
            "mass": "mass",
            "z": "charge",
            "dens": "dens",
            "temp": "temp",
            "a_lt": "omt",
            "a_ln": "omn",
        }

        return pyro_gene_species

    def add_flags(self, pyro, flags):
        """
        Add extra flags to GENE input file

        """

        for key, parameter in flags.items():
            for param, val in parameter.items():
                pyro.gene_input[key][param] = val

    def load_numerics(self, pyro, gene):
        """
        Load Numerics object from pyro.gene_input

        """
        # Need shear for map theta0 to kx
        # shat = pyro.miller['shat']
        # Fourier space grid
        # Linear simulation

        numerics = Numerics()

        # Set number of fields
        numerics.phi = True

        numerics.apar = gene["general"].get("beta", 0) > 0
        numerics.bpar = gene["general"].get("bpar", False)

        numerics.delta_time = gene["general"].get("DELTA_T", 0.01)
        numerics.max_time = gene["general"].get("simtimelim", 500.0)

        numerics.nky = gene["box"]["nky0"]
        numerics.ky = gene["box"]["kymin"]

        try:
            numerics.kx = 2 * pi / gene["box"]["lx"]
        except KeyError:
            numerics.kx = 0.0

        # Velocity grid

        try:
            numerics.ntheta = gene["box"]["nz0"]
        except KeyError:
            numerics.ntheta = 24

        try:
            numerics.nenergy = 0.5 * gene["box"]["nv0"]
        except KeyError:
            numerics.nenergy = 8

        try:
            numerics.npitch = gene["box"]["nw0"]
        except KeyError:
            numerics.npitch = 16

        try:
            nl_mode = gene["nonlinear"]
        except KeyError:
            nl_mode = 0

        if nl_mode == 1:
            numerics.nonlinear = True
            numerics.nkx = gene["box"]["nx0"]
            numerics.nperiod = 1
        else:
            numerics.nonlinear = False
            numerics.nkx = 1
            numerics.nperiod = gene["box"]["nx0"] - 1

        pyro.numerics = numerics

    def load_gk_output(self, pyro, gene_output_number="0000"):
        """
        Loads GKOutput for a given GENE run
        """

        pyro.gk_output = GKOutput()
        pyro.gene_output_number = gene_output_number

        self.load_grids(pyro)

        self.load_fields(pyro)

        self.load_fluxes(pyro)

        if not pyro.numerics.nonlinear:
            self.load_eigenvalues(pyro)

            self.load_eigenfunctions(pyro)

    def load_grids(self, pyro):
        """
        Loads GENE grids to GKOutput

        """

        import xarray as xr

        gk_output = pyro.gk_output

        parameters_file = os.path.join(
            f"{pyro.run_directory}", f"parameters_{pyro.gene_output_number}"
        )
        nml = f90nml.read(parameters_file)

        ntime = nml["info"]["steps"][0] // nml["in_out"]["istep_field"] + 1
        delta_t = nml["info"]["step_time"][0]
        time = np.linspace(0, delta_t * (ntime - 1), ntime)

        gk_output.time = time
        gk_output.ntime = ntime

        field = ["phi", "apar", "bpar"]
        nfield = nml["info"]["n_fields"]

        field = field[:nfield]

        nky = nml["box"]["nky0"]

        nkx = nml["box"]["nx0"]

        ntheta = nml["box"]["nz0"]
        theta = np.linspace(-pi, pi, ntheta, endpoint=False)

        nenergy = nml["box"]["nv0"]
        energy = np.linspace(-1, 1, nenergy)

        npitch = nml["box"]["nw0"]
        pitch = np.linspace(-1, 1, npitch)

        moment = ["particle", "energy", "momentum"]
        species = pyro.local_species.names

        if not pyro.numerics.nonlinear:

            # Set up ballooning angle
            single_theta_loop = theta
            single_ntheta_loop = ntheta

            ntheta = ntheta * (nkx - 1)
            theta = np.empty(ntheta)
            start = 0
            for i in range(nkx - 1):
                pi_segment = i - nkx // 2 + 1
                theta[start : start + single_ntheta_loop] = (
                    single_theta_loop + pi_segment * 2 * pi
                )
                start += single_ntheta_loop

            ky = [nml["box"]["kymin"]]

            kx = [0.0]
            nkx = 1

        # Grid sizes
        gk_output.nky = nky
        gk_output.nkx = nkx
        gk_output.nenergy = nenergy
        gk_output.npitch = npitch
        gk_output.ntheta = ntheta
        gk_output.nspecies = pyro.local_species.nspec
        gk_output.nfield = nfield

        # Grid values
        gk_output.ky = ky
        gk_output.kx = kx
        gk_output.energy = energy
        gk_output.pitch = pitch
        gk_output.theta = theta

        # Store grid data as xarray DataSet
        ds = xr.Dataset(
            coords={
                "time": time,
                "field": field,
                "moment": moment,
                "species": species,
                "kx": kx,
                "ky": ky,
                "theta": theta,
            }
        )

        gk_output.data = ds

    def load_fields(self, pyro):
        """
        Loads 3D fields into GKOutput.data DataSet
        pyro.gk_output.data['fields'] = fields(field, theta, kx, ky, time)
        """

        import struct

        gk_output = pyro.gk_output
        data = gk_output.data

        run_directory = pyro.run_directory

        field_file = os.path.join(run_directory, f"field_{pyro.gene_output_number}")

        fields = np.empty(
            (
                gk_output.nfield,
                gk_output.ntheta,
                gk_output.nkx,
                gk_output.nky,
                gk_output.ntime,
            ),
            dtype=np.complex,
        )

        # Time data stored as binary (int, double, int)
        time = []
        time_data_fmt = "=idi"
        time_data_size = struct.calcsize(time_data_fmt)

        int_size = 4
        complex_size = 16

        nx = pyro.gene_input["box"]["nx0"]
        nz = pyro.gene_input["box"]["nz0"]

        field_size = nx * nz * gk_output.nky * complex_size

        sliced_field = np.empty(
            (gk_output.nfield, nx, gk_output.nky, nz, gk_output.ntime), dtype=np.complex
        )

        fields = np.empty(
            (
                gk_output.nfield,
                gk_output.nkx,
                gk_output.nky,
                gk_output.ntheta,
                gk_output.ntime,
            ),
            dtype=np.complex,
        )

        if os.path.exists(field_file):

            file = open(field_file, "rb")

            for i_time in range(gk_output.ntime):
                # Read in time data (stored as int, double int)
                time_value = float(
                    struct.unpack(time_data_fmt, file.read(time_data_size))[1]
                )

                time.append(time_value)

                for i_field in range(gk_output.nfield):
                    dummy = struct.unpack("i", file.read(int_size))

                    binary_field = file.read(field_size)

                    raw_field = np.frombuffer(binary_field, dtype=np.complex128)

                    sliced_field[i_field, :, :, :, i_time] = np.reshape(
                        raw_field, (nx, gk_output.nky, nz), "F"
                    )

                    dummy = struct.unpack("i", file.read(int_size))  # noqa

            if pyro.numerics.nonlinear:
                fields = np.reshape(
                    sliced_field,
                    (
                        gk_output.nfield,
                        gk_output.nkx,
                        gk_output.ntheta,
                        gk_output.nky,
                        gk_output.ntime,
                    ),
                    "F",
                )

            # Convert from kx to ballooning space
            else:
                i_ball = 0

                for i_conn in range(-int(nx / 2) + 1, int((nx - 1) / 2) + 1):
                    fields[:, 0, :, i_ball : i_ball + nz, :] = (
                        sliced_field[:, i_conn, :, :, :] * (-1) ** i_conn
                    )
                    i_ball += nz

        else:
            print(f"No field file for {field_file}")
            fields[:, :, :, :, :] = None

        data["time"] = time
        gk_output.time = time
        data["fields"] = (("field", "kx", "ky", "theta", "time"), fields)

    def load_fluxes(self, pyro):
        """
        Loads fluxes into GKOutput.data DataSet
        pyro.gk_output.data['fluxes'] = fluxes(species, moment, field, ky, time)
        """

        import csv

        gk_output = pyro.gk_output
        data = gk_output.data

        run_directory = pyro.run_directory
        flux_file = os.path.join(run_directory, f"nrg_{pyro.gene_output_number}")

        fluxes = np.empty((gk_output.nspecies, 3, gk_output.nfield, gk_output.ntime))

        parameters_file = os.path.join(
            f"{pyro.run_directory}", f"parameters_{pyro.gene_output_number}"
        )
        nml = f90nml.read(parameters_file)

        flux_istep = nml["in_out"]["istep_nrg"]
        field_istep = nml["in_out"]["istep_field"]

        if flux_istep < field_istep:
            time_skip = int(field_istep / flux_istep) - 1
        else:
            time_skip = 0

        if os.path.exists(flux_file):

            csv_file = open(flux_file)
            nrg_data = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)

            if gk_output.nfield == 3:
                print("Warning GENE combines Apar and Bpar fluxes")
                fluxes[:, :, 2, :] = 0.0
                field_size = 2
            else:
                field_size = gk_output.nfield

            for i_time in range(gk_output.ntime):

                time = next(nrg_data)  # noqa

                for i_species in range(gk_output.nspecies):
                    nrg_line = np.array(next(nrg_data), dtype=np.float)

                    # Particle
                    fluxes[i_species, 0, :field_size, i_time] = nrg_line[
                        4 : 4 + field_size
                    ]

                    # Energy
                    fluxes[i_species, 1, :field_size, i_time] = nrg_line[
                        6 : 6 + field_size
                    ]

                    # Momentum
                    fluxes[i_species, 2, :field_size, i_time] = nrg_line[
                        8 : 8 + field_size
                    ]

                # Skip time/data values in field print out is less
                if i_time != gk_output.ntime - 1:
                    for skip_t in range(time_skip):
                        for skip_s in range(gk_output.nspecies + 1):
                            next(nrg_data)

        else:
            print(f"No flux file for {flux_file}")
            fluxes[:, :, :, :] = None

        data["fluxes"] = (("species", "moment", "field", "time"), fluxes)
