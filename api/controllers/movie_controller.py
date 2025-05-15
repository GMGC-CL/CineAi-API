from api.models.movie_model import Movie
#importa as funcoes 
from api.controllers.movies_functions import transform_to_json
#importacoes para gerar as indicacoes
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from api.database.connection import get_db
from api.controllers.movies_functions import get_password_hash, verify_password, create_access_token

# Chave secreta e algoritmo para o JWT
SECRET_KEY = "your_secret_key"  # Troque por uma chave secreta segura
ALGORITHM = "HS256"

# Inicialização do contexto do Passlib para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Api:
    #API que irá indicar os filmes retornando os 20 primeiros 
    def cousine_movies(self,filme:int,limite:int):
        #def cousine_movies - função que irá indicar os filmes mais parecidos
        try:
            if not isinstance(filme, int):
                raise TypeError("Valor de ID inválido")
            #passa todos os objetos do banco de dados para json
            jMovies = [transform_to_json(i) for i in Movie.get_all(2668)]
            #transforma tudo em dataframe
            dfMovie = pd.json_normalize(jMovies)
            #concatena todos as informaçòes dos filmes em uma coluna
            dfMovie['Infos'] = dfMovie['generos'] + str(dfMovie['sinopse']) + dfMovie['tags']
            #cria uma classe de vetorização
            vec = TfidfVectorizer()
            #transforma os dados em uma matriz de termos
            tfidf = vec.fit_transform(dfMovie['Infos'].apply(lambda x: np.str_(x)))
            #calcula a similaridade entre os filmes
            sim = cosine_similarity(tfidf)
            sim_df2 = pd.DataFrame(sim, columns=dfMovie['id_filme_tmdb'], index=dfMovie['titulo'])
            # Pegando os filmes mais parecidos com o filme passado na função
            sim_series = sim_df2[filme].sort_values(ascending=False)
            # Transformando em DataFrame
            dfCosine = pd.DataFrame(sim_series).rename(columns={filme: 'similaridade'})
            # Adicionando a coluna 'id_filme_tmdb' ou outras infos
            dfCosine = dfCosine.join(dfMovie.set_index('titulo')[['id_filme_tmdb']])
            #adiciona todas as colunas para retornar para o front
            dfFinal = pd.merge(dfCosine, dfMovie, how='inner', on='id_filme_tmdb')
            #retorna os 20 filmes mais parecidos
            return dfFinal[0:limite].to_dict(orient='records')
        except TypeError as e:
            print(e)
            print('Não foi possível encontrar o filme')
            return False
        except Exception as e:
            import traceback
            print('Ocorreu um erro ao entregar os filmes :(')
            traceback.print_exc()
            return False
        
    #API que irá retornar todos os filmes
    def get_all_movies(self,limit_query:int):
        """
            get_all_movies - função para retornar todos os filmes do banco

            :params limit_query: limite de filmes retornados do banco de dados

            :return: retorna uma lista de objetos de todos os filmes
        """
        try:
            #passa todos os objetos do banco de dados para json
            jMovies = [transform_to_json(i) for i in Movie.get_all(limit_query)]
            #retorna todos os filmes
            return jMovies
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
   
   #API que irá retornar todos os generos
    def get_all_genres(self):
        """
            get_all_genres - função para retornar todos os genero do banco

            :return: retorna uma lista de objetos de todos os generos
        """
        try:
            #passa todos os objetos do banco de dados para json
            jGenres = [transform_to_json(i) for i in Movie.get_genre()]
            #retorna todos os generos
            return jGenres
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os generos')
            return False
        
    #API que irá retornar os filmes filtrados por generos
    def get_movies_for_genre(self,genre_id:str, limit_query:int):
        """
            get_movies_for_genre - função que retorna os filmes filtrados por generos

            :params genre_id: id do genêro que deve ser filtrado
            :params limit_query: limite de filmes retornados do banco de dados

            :return: retorna uma lista de objetos de todos os filmes filtrados por genero
        """
        try:
            #passa todos os objetos do banco de dados para json
            jMovies = [transform_to_json(i) for i in Movie.get_movie_for_genre(genre_id, limit_query)]
            #retorna todos os filmes filtrados por generos
            return jMovies
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
    #API que irá retornar os filmes filtrados pelo nome
    def get_movies_for_name(self,movie_name:str):
        """
            get_movies_for_name - função que retorna o filme pelo nome

            :params movie_name: nome do filme que voce deseja buscar

            :return: retorna todas informações do filme pesqiusado ou retorna None
        """
        try:
            #passa todos os objetos do banco de dados para json
            jMovies = [transform_to_json(i) for i in Movie.get_movie_for_name(movie_name)]
            #retorna todos os filmes filtrados pelo nome
            return jMovies
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
    #API que irá retornar os filmes filtrados pelo id
    def get_movie_by_id(self,movie_id:int):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params movie_name: nome do filme que voce deseja buscar

            :return: retorna todas informações do filme pesqiusado ou retorna None
        """
        try:
            #passa todos os objetos do banco de dados para json
            jMovies = [transform_to_json(i) for i in Movie.get_movie_for_id(movie_id)]
            #retorna todos os filmes filtrados pelo id
            return jMovies
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
    

    def registrar_avaliacao(self,usuario_id:str, filme_id:str, nota:str, comentario:str):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params usuario_id: id do usuario que ta fazendo a avaliacao
            :params filme_id: id do filme
            :params nota: nota total do usuario
            :params comentario: comentario da avaliacao

            :return: retorna true em caso de sucesso
        """
        try:
            #passa todos os objetos do banco de dados para json
            Movie.registrar_avaliacao(usuario_id,filme_id,nota,comentario)
            #retorna todos os filmes filtrados pelo id
            return True
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False

    def get_avaliacao(self,movie_id:str):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params movie_id: id do filme para consulta

            :return: retorna true em caso de sucesso
        """
        try:
            #passa todos os objetos do banco de dados para json
            jAvalicoes = Movie.get_avaliacao(movie_id)
            #retorna todos os filmes filtrados pelo id
            return [transform_to_json(i) for i in jAvalicoes]
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
    
    def registrar_usuario(self,nome:str, email: str, senha: str):
        """
            registrar_usuario - função que registra um novo usuário
            :params email: email do usuario
            :params senha: senha do usuario
            :return: retorna true em caso de sucesso
            
            :raises ValueError: se o email ou senha não forem fornecidos"""
        if not email or not senha or not nome:
            raise ValueError("Email, senha e nome são obrigatórios")

        hashed_password = get_password_hash(senha)
        try:
            #passa todos os objetos do banco de dados para json
            Movie.registrar_usuario(nome, email, hashed_password)
            return True
        except Exception as e:
            print(e)
            print('Não foi possível registrar o usuário')
            return False
        
    def autenticar_usuario(self,email: str, senha: str):
        """
            autenticar_usuario - função que autentica um usuário e gera um token JWT
            
            :params email: email do usuario
            :params senha: senha do usuario

            :return: retorna o token de acesso
        """
        usuario = Movie.autenticar_usuario(email)
        usuario = [transform_to_json(i) for i in usuario]
        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

        if not verify_password(senha, usuario[0]['senha']):  # Verificando se a senha fornecida corresponde ao hash
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

        # Gerando o token JWT
        token = create_access_token(data={"sub": email})

        return {"user": usuario[0]['email'], "token": token, "id": usuario[0]['id_usuario']}
    


    def regitrar_preferencia(self,usuario_id:str, filme_id:str):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params usuario_id: id do usuario que ta guardando o filme
            :params filme_id: id do filme

            :return: retorna true em caso de sucesso
        """
        try:
            #passa todos os objetos do banco de dados para json
            Movie.put_preference(usuario_id,filme_id)
            #retorna todos os filmes filtrados pelo id
            return True
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
        
    def get_preference(self,user_id:int):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params user_id: id do usuario que tem as preferencias

            :return: retorna true em caso de sucesso
        """
        try:
            #passa todos os objetos do banco de dados para json
            jAvalicoes = Movie.get_preference(user_id)
            #retorna todos os filmes filtrados pelo id
            return [transform_to_json(i) for i in jAvalicoes]
        except Exception as e:
            print(e)
            print('Não foi possível encontrar os filmes')
            return False
