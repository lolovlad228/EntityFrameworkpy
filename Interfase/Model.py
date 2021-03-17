class Model:
    @classmethod
    def __str__(cls):
        return f"{cls.__name__} id: {cls.__dict__['id']}"

    @classmethod
    def __repr__(cls):
        return f"{cls.__name__} id: {cls.__dict__['id']}"

    @classmethod
    def name_model(cls):
        return cls.__name__

    @classmethod
    def create_property(cls, value=None):
        end = filter(lambda x: x[:2] != "__" and x[-2:] != "__", cls.__dict__.keys())
        property_model = {}
        for i, y in zip(end, value):
            property_model[i] = y
        return property_model

    @classmethod
    def create_model(cls, val):
        return type(cls.name_model(), (Model,), cls.create_property(val))

    @classmethod
    def len(cls):
        end = list(filter(lambda x: x[:2] != "__" and x[-2:] != "__", cls.__dict__.keys()))
        return len(end)

    @classmethod
    def val_property(cls):
        end = list(filter(lambda x: x[:2] != "__" and x[-2:] != "__", cls.__dict__.keys()))
        info = []
        for i in end:
            info.append(cls.__dict__[i])
        return info
