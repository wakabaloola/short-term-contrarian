from tabulate import tabulate
import json
import os

class ParameterEnvironment:
    ''' A class that can be used to specify and store parameter values. It requires the packages 'tabulate', 'numpy', 'json' and 'os' to be installed.

    Attributes:
    ===========
        Y: dict
            an optional dictionary argument

        **kwargs: key-value pairs
            a variable number of key-value pairs (e.g.: S0=100, K=110, ...)

    Methods:
    ========
        add(key=value): key=value
            Adds a key-value pair to self.parameters.


        update(key=value): key=value
            Updates self.parameters[key] to 'value' if key already exists.

        get(key): value
            Returns 'value' associated with the given key.

        delete(key):
            Deletes key-value pair.

        delete_all():
            Deletes all contents (parameters and descriptions) of the corresponding instance

        get_all():
            Returns all parameter values as a tuple.

        get_keys(): keys
            Returns a list of all stored 'keys'

        is_empty(): bool
            Returns True is ParameterEnvironment instance is empty

        add_description(key=str):
            Adds a parameter description.

        get_description(key):
            Returns parameter description as a string.

        header:
            Sets header to be ued in echo() method, default is headers = ('Description', 'Symbol', 'Value', 'dtype').

        echo:
            Displays all currently stored parameters together with their values and data types.

        to_json('filename.json'):
            Saves all currently stored parameters and descriptions to a JSON file 'filename.json'.

        load_json('filename.json'):
            Loads the parameter and descrtiptions from a user-provided JSON file, 'filename.json'

        to_dataframe():


    Usage example 1:
    ================

    >> env = ParameterEnvironment(S0=100, K=110, T=1, r=0.1, sigma=0.2)
    >> print(env.get('S0'))
    100
    >> print(env.parameters)
    {'S0': 100, 'K': 110, 'T': 1, 'r': 0.1, 'sigma': 0.2}


    Usage example 2:
    ================

    >> from call_option import EuropeanCallOption
    >> from parameters import ParameterEnvironment
    >> env = ParameterEnvironment(S0=100., K=105., T=1., r=0.05, sigma=0.2)
    >> call = EuropeanCallOption(env)
    >> print(call.value())
    >> 8.021352235143176
    '''
    def __init__(self, Y={}, **kwargs):
        if not isinstance(Y, dict):
            raise TypeError("TypeError in '__init__': the object Y should be of type 'dict'.")

        self.parameters = dict(kwargs)
        self.description = dict()

        for key in Y:
            if key in self.parameters:
                raise KeyError(f"KeyError in '__init__': the key {key} is already present in the provided key-value pairs.")

        self.parameters.update(Y)

        self.headers = tuple()


    #===================== Add, update, get and delete parameters ====================#

    def add(self, Y={}, **kwargs):
        '''Adds new key-value pairs to the parameters dictionary.

        Examples 1:
        ===========
        >> from parameters import ParameterEnvironment
        >> env = ParameterEnvironment()
        >> env.parameters
        {}
        >> env.add(A=1, B=2)
        >> env.parameters
        {'A': 1, 'B': 2}

        Example 2:
        ==========
        >> env.parameters
        {'A': 1, 'B': 2}
        >> Y = dict(C=3, D=4)
        >> env.add(Y)
        >> env.parameters
        {'A': 1, 'B': 2, 'C'=3, 'D'=4}
        '''
        if not isinstance(Y, dict):
            raise TypeError("TypeError in 'add': the object Y should be of type 'dict'.")

        for key, value in kwargs.items():
            if key not in self.parameters:# and not isinstance(value, tuple):
                self.parameters[key] = value
                #elif key not in self.parameters and isinstance(value, tuple) and len(value) == 2 and type(value[1] == str):
                #    self.parameters[key] = value[0]
                #    self.description[key] = value[1]
            else:
                raise KeyError(f"KeyError in 'add': the key '{key}' is already present in the dictionary. To update its value use the 'update' method.")

        for key in Y:
            if key in self.parameters:
                raise KeyError(f"KeyError in 'add': the key '{key}' is already present in the provided key-value pairs.")

        self.parameters.update(Y)


    def update(self, **kwargs):
        '''Updates existing parameter values.

        Example:
        ========
        >> env.parameters
        {'A'=1, 'B'=2}
        >> env.update(A=3)
        >> env.parameters
        {'A'=3, 'B'=2}
        '''
        for key, value in kwargs.items():
            if key in self.parameters:
                self.parameters[key] = value
            else:
                raise KeyError(f"KeyError in 'update': the key '{key}' does not yet exist.")


    def get(self, key: str):
        '''Retrieves the value associated with a given key.

        Example:
        ========
        >> env.parameters
        {'A'=3, 'B'=2}
        >> env.get('A')
        3
        '''
        if not isinstance(key, str):
            raise TypeError("TypeError in 'get': ensure the provided key is of type 'str'.")

        if key in self.parameters:
            return self.parameters[key]
        else:
            raise KeyError(f"KeyError in 'get': the parameter {key} does not yet exist.")


    def delete(self, *args: str):
        '''Deletes a key-value pair.

        Example:
        ========
        >> env.parameters
        {'A'=3, 'B'=2, 'C'=3}
        >> env.delete('A', 'B')
        >> env.parameters
        {'C'=3}
        '''
        for key in args:
            if not isinstance(key, str):
                raise TypeError("TypeError in 'delete': ensure the provided key is of type 'str'.")

            self.parameters.pop(key, None)


    def delete_all(self) -> None:
        '''Deletes all contents from the parameters and description dictionaries based on user input.

        Example:
        ========
        >> env.parameters
        {'A'=1, 'B'=2, 'C'=3}
        >> env.delete_all()
        Delete all contents from the 'parameters' and 'description' dictionaries? (y/n) y
        >> env.parameters
        {}
        '''
        answer = input("Delete all contents from the 'parameters' and 'description' dictionaries? (y/n) ")
        if answer.lower() == 'y' or answer.lower() == 'yes' or answer == '':
            self.parameters.clear()
            self.description.clear()
        else:
            pass


    def get_all(self) -> tuple:
        '''Retrieves all parameters as a tuple.

        Example:
        ========
        >> env.parameters
        {'A'=1, 'B'=2, 'C'=3}
        >> A, B, C = env.get_all()
        >> A
        1
        '''
        return tuple(self.parameters[key] for key, value in self.parameters.items())


    def get_keys(self) -> list:
        ''' Retrieves all stored keys as a list
        '''
        keys = list(key for key in self.parameters)
        return keys


    def is_empty(self) -> bool:
        '''Returns True if ParameterEnvironment instance is empty
        '''
        if self.parameters == dict() and self.description == dict():
            return True
        else:
            return False


    #======================= Add, delete and get parameter descriptions =====================#

    def add_description(self, key=None, description=None, **kwargs):
        '''Adds a description for a specific parameter.
        '''
        if key is not None and description is not None:
            if not isinstance(key, str):
                raise TypeError(f"TypeError in 'add_description': provided key must be of type 'str'.")

            if not isinstance(description, str):
                raise TypeError(f"TypeError in 'add_description': provided description must be of type 'str'.")

            if key in self.parameters:
                self.description[key] = description
            else:
                raise KeyError(f"You are trying to add a description of a parameter, {key}, that does not yet exist.")

        if kwargs:
            for key, description in kwargs.items():

                if not isinstance(key, str):
                    raise TypeError(f"TypeError in 'add_description': provided key must be of type 'str'.")

                if not isinstance(description, str):
                    raise TypeError(f"TypeError in 'add_description': provided description must be of type 'str'.")

                if key in self.parameters:
                    self.description[key] = description
                else:
                    raise KeyError(f"You are trying to add a description of a parameter, {key}, that does not yet exist.")


    def delete_description(self, key):
        '''Deletes the description of a parameter.  If all descriptions are deleted then the resulting 'description' column in the 'echo' method is deleted.
        '''
        if not isinstance(key, str):
            raise TypeError(f"TypeError in 'add_description': the provided key must be of type 'str'.")

        if key in self.description:
            self.description[key] = "None"

        descriptions_none = all(map(lambda x: x == "None", self.description.values()))
        if descriptions_none:
            self.description = dict()


    def get_description(self, key):
        '''Retrieves the description of a parameter.
        '''
        if not isinstance(key, str):
            raise TypeError(f"TypeError in 'add_description': the provided key must be of type 'str'.")

        if key in self.parameters:
            try:
                return self.description[key]
            except KeyError:
                return "None"
        else:
            raise KeyError(f"KeyError in 'get_description': the key '{key}' does not yet exist.")


    def merge(self, *instances):
        '''Merges instance into "self" instance

        Usage example:
        ==============
        Merging 'outs' instance into 'ins' instance:

            >> ins = ParameterEnvironment(A=1, B=2)
            >> outs = ParameterEnvironment(C=3, D=4)
            >> outs.add_description(C="An informative description of C")
            >> ins.merge(outs)
            >> ins.echo()
            +---------------------------------+----------+---------+---------+
            | Description                     | Symbol   |   Value | dtype   |
            +=================================+==========+=========+=========+
            | None                            | A        |       1 | int     |
            +---------------------------------+----------+---------+---------+
            | None                            | B        |       2 | int     |
            +---------------------------------+----------+---------+---------+
            | An informative description of C | C        |       3 | int     |
            +---------------------------------+----------+---------+---------+
            | None                            | D        |       4 | int     |
            +---------------------------------+----------+---------+---------+
        '''
        for instance in instances:
            if isinstance(instance, ParameterEnvironment):
                for key, value in instance.parameters.items():
                    self.add({key: value})
                for key, value in instance.description.items():
                    self.add_description(key=key, description=value)
            else:
                raise ValueError(f"ValueError in 'merge': the argument of merge should be a 'ParameterEnvironment' class instance.")


    #======================== Echo all parameter information ========================#
    def header(self, *headers):
        '''Set header to default if no arguments provided'''
        if len(headers) == 0:
            self.headers = tuple()
            '''If the incorrect number of arguments is provided raises ValueError:'''
        elif len(headers) != 4:
            raise ValueError("ValueError in 'echo': 'headers' requires 4 entries, the default is headers = ('Description', 'Symbol', 'Value', 'dtype')")
            '''Finally, if 4 arguments of type str are provided, store them in a new header tuple:'''
        elif len(headers) == 4 and all(isinstance(header, str) for header in headers):
            self.headers = tuple(headers)
        else:
            raise ValueError("ValueError in 'echo': All 4 header entries must be of type 'str'")


    def echo(self, dtype=True, description=True, colwidth=35, tableformat="simple_grid"):
        '''Displays all stored parameters, their values, data types, and descriptions (if available) in a tabulated format.

        Arguments:
        ===========
        dtype: True or False
                Option to display the datatype in the table

        description: True or False
                Option to display the parameter description (if it is present) in the table

        colwidth: column width (in number of characters)
                Max width of the 'description' column

        tableformat: grid, simple_grid, rounded_grid, heavy_grid, mixed_grid, double_grid, fancy_grid, outline, simple_outline, rounded_outline, etc.
                Various choices for the table format
        '''
        if self.is_empty():
            print(f"This instance of ParameterEnvironment is emtpy.")
        if not self.headers:
            headers = ("Description", "Symbol", "Value", "dtype")
        else:
            headers = self.headers
        table = []
        if self.description and description and dtype:
            for key, value in self.parameters.items():
                table.append([self.get_description(key), key, value, type(value).__name__])
            print(tabulate(table, headers=headers[0:4], maxcolwidths=[colwidth, None, None, None], tablefmt=tableformat))
        elif dtype:
            for key, value in self.parameters.items():
                table.append([key, value, type(value).__name__])
            print(tabulate(table, headers[1:4], tablefmt=tableformat))
        elif self.description and description:
            for key, value in self.parameters.items():
                table.append([self.get_description(key), key, value])
            print(tabulate(table, headers[0:3], maxcolwidths=[colwidth, None, None], tablefmt=tableformat))
        else:
            for key, value in self.parameters.items():
                table.append([key, value])
            print(tabulate(table, headers[1:3], maxcolwidths=[colwidth, None], tablefmt=tableformat))


    #============== Save/load parameter and description dictionaries to/from JSON =============#

    def to_json(self, filename=None):
        '''Saves the parameters and their descriptions to a JSON file with the user-provided filename.
        '''
        if filename == None:
            print("A filename for the JSON file must be provided as an argument in the to_json method.")
            return 

        if not isinstance(filename, str):
            raise TypeError("TypeError in 'to_json': 'filename' must be of type 'str'.")

        json_dict = dict()
        for key, value in self.parameters.items():
            if key in self.description:
                json_dict[key] = dict(value=value, description=self.description[key])
            else:
                json_dict[key] = dict(value=value)

        with open(filename, 'w') as file:
            json.dump(json_dict, file, indent=4)


    def load_json(self, filename):
        '''Loads parameters and descriptions from a JSON file (with the user-provided filename) into the parameters and description dictionaries.
        '''
        if not isinstance(filename, str):
            raise TypeError("TypeError in 'load': 'filename' must be of type 'str'.")

        if not os.path.exists(filename):
            raise FileNotFoundError(f"FileNotFoundError in 'load': filename '{filename}' does not exist.")

        with open(filename, 'r') as file:
            loaded_dict = json.load(file)
            if self.is_empty():
                for key in loaded_dict:
                    if "value" not in loaded_dict[key]:
                        raise ValueError(f"ValueError in 'load': the key 'value' must be present in {filename}.")

                    self.parameters[key] = loaded_dict[key]["value"]
                    if "description" in loaded_dict[key]:
                        self.description[key] = loaded_dict[key]["description"]
            else:
                raise ValueError(f"ValueError in 'load': the ParameterEnvironment instance you are trying to load the JSON file {filename} into is not empty.")


def main():
    env = ParameterEnvironment(S0=100, K=110, T=1, r=0.1, sigma=0.2)
    env.add_description('S0', "Stock/index price")
    env.add_description('K', "Strike price at maturity")
    env.add_description('T', "Time to maturity")
    env.add_description('r', "Constant risk-free short interest rate")
    env.add_description('sigma', "Volatility factor in diffusion term")
    env.echo(dtype=False)
    S0, K, T, r, sigma = env.get_all()
    #print(S0, K, T, r, sigma)

if __name__ == "__main__":
    main()


