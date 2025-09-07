from Repositories.PokemonRepositories import PokemonRepository

class PokemonService:
    def __init__(self):
        self.repository = PokemonRepository()
    
    def create_pokemon(self, pokemon_data):
        try:
            # Validar datos
            required_fields = ['nombre', 'tipo', 'nivel', 'poder_ataque', 'poder_defensa', 'hp']
            for field in required_fields:
                if field not in pokemon_data:
                    raise ValueError(f"El campo {field} es requerido")
            
            # Validar tipos de datos
            if not isinstance(pokemon_data['nivel'], int) or pokemon_data['nivel'] <= 0:
                raise ValueError("El nivel debe ser un número entero positivo")
            
            if not isinstance(pokemon_data['hp'], int) or pokemon_data['hp'] <= 0:
                raise ValueError("El HP debe ser un número entero positivo")
            
            pokemon = self.repository.create_pokemon(pokemon_data)
            return pokemon.to_dict()
        except Exception as e:
            raise Exception(f"Error al crear el Pokémon: {str(e)}")
    
    def get_all_pokemons(self):
        pokemons = self.repository.get_all_pokemons()
        return [pokemon.to_dict() for pokemon in pokemons]
    
    def get_pokemon_by_id(self, pokemon_id):
        pokemon = self.repository.get_pokemon_by_id(pokemon_id)
        if pokemon:
            return pokemon.to_dict()
        return None
    
    def update_pokemon(self, pokemon_id, pokemon_data):
        pokemon = self.repository.update_pokemon(pokemon_id, pokemon_data)
        if pokemon:
            return pokemon.to_dict()
        return None
    
    def delete_pokemon(self, pokemon_id):
        return self.repository.delete_pokemon(pokemon_id)