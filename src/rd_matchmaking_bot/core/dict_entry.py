from dataclasses import dataclass, asdict

@dataclass
class DictEntry:
    """
    Represents a ``str`` key to ``dict`` value pair.

    Subclass variables are used as the value's properties.
    """

    __key: str

    @property
    def key(self):
        """**Read-only** key string."""

        return self.__key

    def to_dict(self, exclude: list[str] = None) -> dict:
        """
        Converts to a ``dict`` in the format ``key: {...}``.

        Specific properties can be omitted via ``exclude``.
        """

        value = asdict(self)
        key = value.pop("_DictEntry__key")

        if exclude is not None:
            for excluded in exclude:
                if excluded in value:
                    value.pop(excluded)

        return {key: value}

    @classmethod
    def from_dict(cls, key: str, value: dict):
        """
        Converts a ``str`` key and ``dict`` value into an object of the calling class.

        This will behave unexpectedly if the ``dict``'s values do not match the class' variables.
        """

        properties = (val for val in value.values())

        # noinspection PyArgumentList
        return cls(key) if cls == __class__ else cls(key, *properties)