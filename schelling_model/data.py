import numpy

from schelling_model.constants import AgentValues
from schelling_model.data_descriptors import OneOf


class Agent:
    value = OneOf(AgentValues)

    def __init__(self, value: str):
        self.value = value.upper()

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r})"


class DataTable(dict):
    class DataColumn(dict):
        def __init__(self, size: int, dict_value: dict = None):
            self.size = size
            super().__init__(dict_value or {})

        def __setitem__(self, key: int, item: str):
            if not isinstance(key, int):
                raise KeyError(
                    f"unsupported index type: {type(key)}({key}), should be int"
                )
            if key >= self.size:
                raise KeyError(f"column index out of bounds: {key}")

            super().__setitem__(key, Agent(item))

        def __getitem__(self, key: int) -> Agent:
            return self.__dict__[key]

        def validate(self):
            if not all([len(self) == self.size, self.get(self.size - 1)]):
                print(self)
                raise ValueError("incorrect column size")

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.__data = {}
        super().__init__()

    def __str__(self) -> str:
        data = self.__data
        matrix = numpy.array(
            [[value for value in row.values()] for row in data.values()]
        ).T.tolist()
        row_list = []
        for index, row in enumerate(matrix):
            row_list.append(f"{index} {' '.join([str(val) for val in row])}")

        table_to_str = f'  {" ".join(str(col) for col in data.keys())}\n'
        return table_to_str + "\n".join(row_list)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(width={self.width!r}, height={self.height!r})"
        )

    def __setitem__(self, key: int, item: dict):
        if not isinstance(item, dict):
            raise TypeError(
                f"unsupported type: {type(item)}({item}), should be dict"
            )
        if not isinstance(key, int):
            raise KeyError(
                f"unsupported index type: {type(key)}({key}), should be int"
            )
        if key >= self.width:
            raise KeyError(f"row index out of bounds: {key}")

        self.__data[key] = self.DataColumn(size=self.height, dict_value=item)

    def __getitem__(self, key: int) -> DataColumn:
        if not isinstance(key, int):
            raise KeyError(
                f"unsupported index type: {type(key)}({key}), should be int"
            )
        if key >= self.width:
            raise KeyError(f"row index out of bounds: {key}")

        # if not self.__data.get(key):
        #     self.__data[key] = self.DataColumn(size=self.height)

        return self.__data[key]

    def validate(self):
        if not all(
            [len(self.__data) == self.width, self.__getitem__(self.width - 1)]
        ):
            raise ValueError("incorrect column size")

        for col in self.__data.values():
            col.validate()

    def populate(self, value=AgentValues.EMPTY):
        if value not in AgentValues:
            raise ValueError(
                f"Expected {value!r} to be one of {AgentValues!r}"
            )

        for col in range(self.width):
            self.__data[col] = {}
            for row in range(self.height):
                self.__data[col][row] = value

    @classmethod
    def load_from_file(cls, file_path) -> "DataTable":
        matrix = []
        with open(file=file_path, mode="r") as file:
            for line in file.readlines():
                matrix.append([char for char in line.strip("\n")])

        if not matrix:
            raise Exception("Empty file")

        expected_row_count = len(matrix)
        expected_col_count = len(matrix[0])

        data_table = DataTable(
            width=expected_col_count, height=expected_row_count
        )

        matrix = numpy.array(matrix).T.tolist()

        for col_count, col_values in enumerate(matrix):
            data_table[col_count] = {}
            for row_count, val in enumerate(col_values):
                data_table[col_count][row_count] = val

        return data_table
