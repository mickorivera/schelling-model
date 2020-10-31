class ConstBaseMeta(type):
    def __init__(cls, *args, **kwargs):
        cls_dict = cls.__dict__
        cls._attributes = tuple(
            cls_dict[k] for k in cls_dict.keys() if not k.startswith("_")
        )
        super().__init__(cls)

    def __getitem__(cls, index):
        return cls._attributes[index]

    def __len__(self):
        return len(self._attributes)

    def __repr__(cls):
        return ",".join(cls._attributes)


class AgentValues(metaclass=ConstBaseMeta):
    X = "X"
    O = "O"
    EMPTY = " "
