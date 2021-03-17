from Models.Goods import Goods
from Interfase import ISolid
from Moduls import EntityClass
from Moduls.DataBase.SqlLite import SqlLite


class DataContext(metaclass=ISolid.Solide):

    data_base = SqlLite("test.db")

    Goods = EntityClass.EntityModel(Goods, data_base)


DataContext().data_base = SqlLite("test.db")

DataContext.Goods.load()

info = DataContext.Goods.where(lambda x: x.Id == 1).first_of_default()

info.Name = "lolo"

DataContext.Goods.update(info)

DataContext.Goods.save_change()


