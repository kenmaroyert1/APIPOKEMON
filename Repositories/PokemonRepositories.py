from Models.Pokemon import Pokemon
from Config.DataBase import db

class PokemonRepository:
    def create_pokemon(self, pokemon_data):
        pokemon = Pokemon(**pokemon_data)
        db.session.add(pokemon)
        db.session.commit()
        return pokemon
    
    def get_all_pokemons(self):
        return Pokemon.query.all()
    
    def get_pokemon_by_id(self, pokemon_id):
        return Pokemon.query.get(pokemon_id)
    
    def update_pokemon(self, pokemon_id, pokemon_data):
        pokemon = Pokemon.query.get(pokemon_id)
        if pokemon:
            for key, value in pokemon_data.items():
                setattr(pokemon, key, value)
            db.session.commit()
        return pokemon
    
    def delete_pokemon(self, pokemon_id):
        pokemon = Pokemon.query.get(pokemon_id)
        if pokemon:
            db.session.delete(pokemon)
            db.session.commit()
            return True
        return False