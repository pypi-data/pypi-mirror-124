import numpy as np
from .pyro import Pyro
import os
from itertools import product
from functools import reduce
import operator
import copy


class PyroScan:
    """
    Creates a dictionary of pyro objects in pyro_dict

    Need a templates pyro object

    Dict of parameters to scan through
    { param : [values], }
    """

    def __init__(
        self,
        pyro,
        parameter_dict=None,
        p_prime_type=0,
        value_fmt=".2f",
        value_separator="_",
        parameter_separator="/",
        file_name=None,
        base_directory=".",
        load_default_parameter_keys=True,
    ):

        # Dictionary of parameters and values
        self.parameter_dict = {}

        # Mapping from parameter to location in Pyro
        self.parameter_map = {}

        # Dictionary of Pyro objects
        self.pyro_dict = {}

        self.base_directory = base_directory

        # Format values/parameters
        self.value_fmt = value_fmt

        self.value_separator = value_separator

        if parameter_separator in ["/", "\\"]:
            self.parameter_separator = os.path.sep
        else:
            self.parameter_separator = parameter_separator

        if load_default_parameter_keys:
            self.load_default_parameter_keys()

        if file_name is not None:
            self.file_name = file_name
        else:
            self.file_name = pyro.gk_code.default_file_name

        self.run_directories = None

        if isinstance(pyro, Pyro):
            self.base_pyro = pyro
        else:
            raise ValueError("PyroScan takes in a pyro object")

        if isinstance(parameter_dict, dict):
            self.parameter_dict = parameter_dict

            pyro_dict = {}

            # Get len of values for each parameter
            self.value_size = [len(value) for value in self.parameter_dict.values()]

            # Outer product of input dictionaries - could get very large
            self.outer_product = list(
                dict(zip(self.parameter_dict, x))
                for x in product(*self.parameter_dict.values())
            )

            # Iterate through all runs and create dictionary
            for run in self.outer_product:

                single_run_name = ""
                # Param value for each run written accordingly
                for param, value in run.items():
                    single_run_name += (
                        f"{param}{self.value_separator}{value:{self.value_fmt}}"
                    )

                    single_run_name += self.parameter_separator

                # Remove last instance of parameter_separator
                single_run_name = single_run_name[: -len(self.parameter_separator)]

                # Store copy of each pyro in a dictionary and set file_name/directory
                pyro_dict[single_run_name] = copy.deepcopy(self.base_pyro)

                pyro_dict[single_run_name].file_name = self.file_name
                pyro_dict[single_run_name].run_directory = os.path.join(
                    self.base_directory, single_run_name
                )

            self.pyro_dict = pyro_dict

            self.run_directories = [pyro.run_directory for pyro in pyro_dict.values()]

        else:
            raise ValueError("PyroScan takes in a dict object")

        self.p_prime_type = p_prime_type

    def write(self, file_name=None, base_directory=None, template_file=None):
        """
        Creates and writes GK input files for parameters in scan
        """

        if file_name is not None:
            self.file_name = file_name

        if base_directory is not None:
            self.base_directory = base_directory

            # Set run directories
            self.run_directories = [
                os.path.join(self.base_directory, run_dir)
                for run_dir in self.pyro_dict.keys()
            ]

        # Iterate through all runs and write output
        for parameter, run_dir, pyro in zip(
            self.outer_product, self.run_directories, self.pyro_dict.values()
        ):
            # Param value for each run written accordingly
            for param, value in parameter.items():

                # Get attribute name and keys where param is stored in Pyro
                (
                    attr_name,
                    keys_to_param,
                ) = self.parameter_map[param]

                # Get attribute in Pyro storing the parameter
                pyro_attr = getattr(pyro, attr_name)

                # Set the value given the Pyro attribute and location of parameter
                set_in_dict(pyro_attr, keys_to_param, value)

            # Write input file
            pyro.write_gk_file(
                file_name=self.file_name, directory=run_dir, template_file=template_file
            )

    def add_parameter_key(
        self, parameter_key=None, parameter_attr=None, parameter_location=None
    ):
        """
        parameter_key: string to access variable
        parameter_attr: string of attribute storing value in pyro
        parameter_location: lis of strings showing path to value in pyro
        """

        if parameter_key is None:
            raise ValueError("Need to specify parameter key")

        if parameter_attr is None:
            raise ValueError("Need to specify parameter attr")

        if parameter_location is None:
            raise ValueError("Need to specify parameter location")

        dict_item = {parameter_key: [parameter_attr, parameter_location]}

        self.parameter_map.update(dict_item)

    def load_default_parameter_keys(self):
        """
        Loads default parameters name into parameter_map

        {param : ["attribute", ["key_to_location_1", "key_to_location_2" ]] }

        for example

        {'electron_temp_gradient': ["local_species", ['electron','a_lt']] }
        """

        self.parameter_map = {}

        # ky
        parameter_key = "ky"
        parameter_attr = "numerics"
        parameter_location = ["ky"]
        self.add_parameter_key(parameter_key, parameter_attr, parameter_location)

        # Electron temperature gradient
        parameter_key = "electron_temp_gradient"
        parameter_attr = "local_species"
        parameter_location = ["electron", "a_lt"]
        self.add_parameter_key(parameter_key, parameter_attr, parameter_location)

        # Electron density gradient
        parameter_key = "electron_dens_gradient"
        parameter_attr = "local_species"
        parameter_location = ["electron", "a_ln"]
        self.add_parameter_key(parameter_key, parameter_attr, parameter_location)

        # Deuterium temperature gradient
        parameter_key = "deuterium_temp_gradient"
        parameter_attr = "local_species"
        parameter_location = ["deuterium", "a_lt"]
        self.add_parameter_key(parameter_key, parameter_attr, parameter_location)

        # Deuterium density gradient
        parameter_key = "deuterium_dens_gradient"
        parameter_attr = "local_species"
        parameter_location = ["deuterium", "a_ln"]
        self.add_parameter_key(parameter_key, parameter_attr, parameter_location)

    def load_gk_output(self):
        """
        Loads GKOutput as a CleverDict

        Returns
        -------
        self.gk_output : CleverDict of data
        self.gk_output.data : xarray DataSet of data
        """

        import xarray as xr
        from cleverdict import CleverDict

        # Set up output as CleverDict
        self.gk_output = CleverDict()

        # xarray DataSet to store data
        ds = xr.Dataset(self.parameter_dict)

        if not self.base_pyro.numerics.nonlinear:
            growth_rate = []
            mode_frequency = []
            eigenfunctions = []

            # Load gk_output in copies of pyro
            for pyro in self.pyro_dict.values():
                pyro.load_gk_output()

                growth_rate.append(pyro.gk_output.data["growth_rate"].isel(time=-1))
                mode_frequency.append(
                    pyro.gk_output.data["mode_frequency"].isel(time=-1)
                )
                eigenfunctions.append(
                    pyro.gk_output.data["eigenfunctions"]
                    .isel(time=-1)
                    .drop_vars(["time"])
                )

            # Save eigenvalues
            growth_rate = np.reshape(growth_rate, self.value_size)
            mode_frequency = np.reshape(mode_frequency, self.value_size)

            ds["growth_rate"] = (self.parameter_dict.keys(), growth_rate)
            ds["mode_frequency"] = (self.parameter_dict.keys(), mode_frequency)

            # Add eigenfunctions
            eig_coords = eigenfunctions[-1].coords
            ds = ds.assign_coords(coords=eig_coords)

            # Reshape eigenfunctions and generate new coordinates
            eigenfunction_shape = self.value_size + list(np.shape(eigenfunctions[-1]))
            eigenfunctions = np.reshape(eigenfunctions, eigenfunction_shape)
            eigenfunctions_coords = tuple(self.parameter_dict.keys()) + eig_coords.dims

            ds["eigenfunctions"] = (eigenfunctions_coords, eigenfunctions)

        self.gk_output["data"] = ds

    @property
    def gk_code(self):
        return self.base_pyro.gk_code

    @gk_code.setter
    def gk_code(self, value):
        """
        Sets the GK code to be used

        """
        self.base_pyro.gk_code = value

        # Set gk_code in copies of pyro
        for pyro in self.pyro_dict.values():
            pyro.gk_code = value

    @property
    def base_directory(self):
        return self._base_directory

    @base_directory.setter
    def base_directory(self, value):
        """
        Sets the base_directory

        """

        self._base_directory = value

        # Set base_directory in copies of pyro
        for key, pyro in self.pyro_dict.items():
            pyro.run_directory = os.path.join(self.base_directory, key)


def get_from_dict(data_dict, map_list):
    """
    Gets item in dict given location as a list of string
    """
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    """
    Sets item in dict given location as a list of string
    """
    get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value
