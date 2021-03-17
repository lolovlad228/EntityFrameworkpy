import pyodbc
from Interfase.Fluent import Fluent
from Interfase.Model import Model


class EntityModel(Fluent):
    def __init__(self, type_model, type_data_base):
        self.__model_info = type_model
        self.__type_data_base = type_data_base

        self.__list_model = []
        self.__hash_table = None
        self.__list_save = []

    def load(self):
        self.__type_data_base.create_link()
        self.__list_model.clear()
        sql_text = """SELECT * FROM """ + self.__model_info.name_model()
        self.__type_data_base.cursor.execute(sql_text)
        result = self.__type_data_base.cursor.fetchall()
        self.__type_data_base.commit_link()
        self.__list_model = list(map(lambda x: self.__model_info.create_model(x), result))
        self.__type_data_base.destroy_link()

    def where(self, lmd):
        self.__hash_table = list(filter(lmd, self.__list_model))

    def first_of_default(self):
        if self.__hash_table is not None:
            if len(self.__hash_table) > 0:
                return self.__hash_table[0]
            else:
                return False
        else:
            return self.__list_model[0]

    def delite(self, model=None):
        if hasattr(model, "name_model"):
            self.__list_save.append((model, "delite"))
        elif model is None:
            for i in self.__hash_table:
                self.__list_save.append((i, "delite"))
        else:
            for i in list(filter(model, self.__list_model)):
                self.__list_save.append((i, "delite"))

    def add(self, model):
        if hasattr(model, "name_model"):
            self.__list_save.append((model, "add"))

    def update(self, model):
        if hasattr(model, "name_model"):
            self.__list_save.append((model, "update"))

    def save_change(self):
        self.__type_data_base.create_link()
        cl_name = self.__type_data_base.name_column_table(self.__model_info.name_model())
        for i in self.__list_save:
            if i[1] == "delite":
                sql = "DELETE FROM " + self.__model_info.name_model() + " WHERE  " + cl_name[0] + " = ?"
                self.__type_data_base.cursor.execute(sql, (i[0].Id, ))
                self.__type_data_base.commit_link()
            elif i[1] == "add":
                str_cl_name = ", ".join(cl_name[1:],)
                value = ", ".join(["?"] * (i[0].len() - 1))
                sql = "INSERT INTO " + self.__model_info.name_model() + " (" + str_cl_name + ") VALUES " \
                      + "(" + value + ")"
                self.__type_data_base.cursor.execute(sql, tuple(i[0].val_property()[1:]))
                self.__type_data_base.commit_link()
            elif i[1] == "update":
                value = ", ".join(["?"] * (i[0].len() - 1))
                value = value.split()
                end_val = ""
                for k, p in zip(cl_name[1:], value):
                    end_val += k + " = " + p
                sql = "UPDATE " + self.__model_info.name_model() + " SET " + end_val + \
                      " WHERE " + cl_name[0] + " = ?"
                args = i[0].val_property()[1:] + [i[0].val_property()[0]]
                self.__type_data_base.cursor.execute(sql, tuple(args))
                self.__type_data_base.commit_link()
        self.__list_save.clear()
        self.__type_data_base.destroy_link()

    def list_model(self):
        if self.__hash_table is None:
            return self.__list_model
        else:
            return self.__hash_table

    # refactor
    def join(self, model_one, model_two, arg):
        self.__list_model.clear()
        name_model_one = model_one.name_model()
        name_model_two = model_two.name_model()
        sql_text = "Select bo.*, u.*, bi.* from \"" + self.__model_info.name_model() + "\" bi " \
                   "Inner Join \"" + name_model_two + "\" u on bi.Id_" + name_model_two + " = u.Id " \
                   "Inner Join \"" + name_model_one + "\" bo on bi.Id_" + name_model_one + " = bo.Id"
        self.__content.execute(sql_text)
        result = self.__content.fetchall()
        self.__link.commit()
        for i in result:
            list_arg = []
            for j in arg:
                list_arg.append(i[j])
            self.__list_model.append(self.__model_info(list_arg))


