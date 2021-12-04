import json


class Pokemon:
    def __init__(self, id_num, name, pkm_type, weaknesses):
        self.pkmn_num = id_num
        self.name = name
        self.pkmn_type = pkm_type
        self.weaknesses = weaknesses

    def get_id_num(self):
        return self.pkmn_num

    def get_name(self):
        return self.name

    def get_pkmn_type(self):
        return self.pkmn_type

    def get_weaknesses(self):
        return self.weaknesses

    def set_id_num(self, id_num_given):
        self.pkmn_num = id_num_given

    def set_name(self, name_given):
        self.name = name_given

    def set_pkm_type(self, type_given):
        self.pkmn_type = type_given

    def set_weaknesses(self, weaknesses_given):
        self.weaknesses = weaknesses_given


class Pokedex:
    def __init__(self):
        self.list_pokemons = []
        f = open("pokedex.json")
        pokemons = json.load(f)
        f.close()
        list_pkmns = pokemons["pokemon"]
        for pkmn in list_pkmns:
            pkmn_id_num = pkmn["id"]
            pkmn_name = pkmn["name"]
            pkmn_type = pkmn["type"]
            pkmn_weaknesses = pkmn["weaknesses"]
            pkm = Pokemon(pkmn_id_num, pkmn_name, pkmn_type, pkmn_weaknesses)
            self.list_pokemons.append(pkm)
