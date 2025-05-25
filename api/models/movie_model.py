# models/movie_model.py
import sqlite3
from api.database.connection import get_db

#classe que retorna todos os filmes
class Movie:
    @staticmethod
    def get_all(limit_query: int):
        """
        get_all - função para retornar todos os filmes do banco

        :params limit_query: limite de filmes retornados do banco de dados

        :return: retorna uma lista de objetos de todos os filmes
        """
        conn = get_db()
        cursor = conn.cursor()
        
        query = """
           SELECT f.*, GROUP_CONCAT(g.nome, ', ') AS generos
                        FROM filmes f
                        JOIN filme_genero fg ON f.id_filme_tmdb = fg.id_filme_tmdb
                        JOIN generos g ON fg.id_genero = g.id_genero
                        GROUP BY f.id_filme_tmdb, f.titulo
                        ORDER BY f.popularidade DESC
                       LIMIT ?
        """
        cursor.execute(query, (limit_query,))
        return cursor.fetchall()

    
    @staticmethod
    def get_genre():
        """
            get_movie_genre - função para retornar todos os genero do banco

            :return: retorna uma lista de objetos de todos os generos
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM generos;")
        return cursor.fetchall()
    
    @staticmethod
    def get_movie_for_genre(genre_id:str,limit_query:int):
        """
            get_movie_for_genre - função que retorna os filmes filtrados por generos

            :params genre_id: id do genêro que deve ser filtrado
            :params limit_query: limite de filmes retornados do banco de dados

            :return: retorna uma lista de objetos de todos os filmes filtrados por genero
        """
        if not isinstance(genre_id, str):
            raise ValueError("Valor de genêro inválido")
        elif not isinstance(limit_query, int):
            raise ValueError("Valor de limite inválido")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT f.*, g.nome
                FROM filmes f
                JOIN filme_genero fg ON f.id_filme_tmdb = fg.id_filme_tmdb
                JOIN generos g ON fg.id_genero = g.id_genero
                WHERE fg.id_genero = {genre_id}
                ORDER BY f.media_votos DESC
                LIMIT {limit_query};""")
        return cursor.fetchall()

    @staticmethod  
    def get_movie_for_name(movie_name:str):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params movie_name: nome do filme que voce deseja buscar

            :return: retorna todas informações do filme pesqiusado ou retorna None
        """
        if not isinstance(movie_name, str):
            raise ValueError("Valor de genêro inválido")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM filmes WHERE titulo LIKE '%{movie_name}%';""")
        retorno = cursor.fetchall()
        if not retorno:
            raise IndexError("Filme não encontrado")
        else:
            return retorno
    
    @staticmethod  
    def get_movie_for_id(movie_id:int):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params movie_name: nome do filme que voce deseja buscar

            :return: retorna todas informações do filme pesqiusado ou retorna None
        """
        if not isinstance(movie_id, int):
            raise ValueError("Valor de genêro inválido")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM filmes WHERE id_filme_tmdb = {movie_id};""")
        retorno = cursor.fetchall()
        if not retorno:
            raise IndexError("Filme não encontrado")
        else:
            return retorno

    @staticmethod  
    def registrar_avaliacao(usuario_id: str, filme_id: str, nota: str, comentario: str):
        """
            registrar_avaliacao - função que insere uma avaliação no banco de dados

            :params usuario_id: id do usuario que está fazendo a avaliação
            :params filme_id: id do filme
            :params nota: nota total do usuário
            :params comentario: comentário da avaliação

            :return: retorna true em caso de sucesso
        """
        try:
            conn = get_db()  # Acessa o banco de dados
            cursor = conn.cursor()

            # Realiza a inserção na tabela de avaliações
            cursor.execute(
                "INSERT INTO avaliacoes (id_usuario, id_filme_tmdb, nota, comentario) VALUES (?, ?, ?, ?)",
                (usuario_id, filme_id, nota, comentario),
            )

            # Realiza o commit para salvar a inserção
            conn.commit()

            # Fecha a conexão após a operação
            conn.close()

            return True

        except Exception as e:
            print(f"Erro ao registrar avaliação: {e}")
            return False

    
    @staticmethod  
    def get_avaliacao(movie_id:str):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params movie_id: id do filme para saber a avaliação

            :return: retorna a avaliação do filme
        """
        if not isinstance(movie_id, str):
            raise ValueError("Valor de genêro inválido")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM avaliacoes WHERE id_filme_tmdb = ?",
        (movie_id,),
            )
        retorno = cursor.fetchall()
        if not retorno:
            raise IndexError("avaliacao não encontrada")
        else:
            return retorno

    @staticmethod
    def registrar_usuario(nome:str, email: str, senha: str):
        """
        registrar_usuario - função para registrar novo usuário
        
        :params email: email do novo usuário
        :params senha: senha do novo usuário
        
        :return: True se sucesso, senão lança erro
        """
        if not email or not senha:
            raise ValueError("Email e senha são obrigatórios")
        
        conn = get_db()
        cursor = conn.cursor()

        # Verifica se o e-mail já existe
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            raise ValueError("E-mail já cadastrado")
        
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        return True

    @staticmethod
    def buscar_usuario_por_email(email: str):
        """
        buscar_usuario_por_email - retorna os dados do usuário pelo e-mail

        :params email: e-mail do usuário

        :return: dados do usuário ou None
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user:
            raise IndexError("Usuário não encontrado")
        return user

    @staticmethod
    def autenticar_usuario(email: str):
        """
        autenticar_usuario - verifica se e-mail e senha estão corretos

        :params email: e-mail do usuário
        :params senha: senha do usuário

        :return: dados do usuário se autenticado, senão erro
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchall()
        if not user:
            raise PermissionError("Credenciais inválidas")
        return user
    
    @staticmethod
    def put_preference(user_id,id_filme):
        """
        registrar_usuario - função para registrar novo usuário
        
        :params user_id: id do usuario
        :params id_filme: id do filme que ele gosta
        
        :return: True se sucesso, senão lança erro
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO preferencias_usuario (usuario_id,filme_id) VALUES (?, ?)",(user_id,id_filme))
        conn.commit()
        return True
    
    @staticmethod  
    def get_preference(user_id:int):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params user_id: id do usuario

            :return: retorna prerencias dos filmes
        """
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM preferencias_usuario WHERE usuario_id = ?",
        (user_id,),
            )
        retorno = cursor.fetchall()
        if not retorno:
            raise IndexError("preferencia não encontrada")
        else:
            return retorno
        

    @staticmethod
    def put_preference_genre(user_id,id_genero):
        """
        registrar_usuario - função para registrar novo usuário
        
        :params user_id: id do usuario
        :params id_filme: id do genero que ele gosta
        
        :return: True se sucesso, senão lança erro
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuario_genero (id_usuario,id_genero) VALUES (?, ?)",(user_id,id_genero))
        conn.commit()
        return True
    
    @staticmethod  
    def get_preference_genre(user_id:int):
        """
            post_movie_for_name - função que retorna o filme pelo nome

            :params user_id: id do usuario

            :return: retorna a genero do usuario
        """
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM usuario_genero WHERE id_usuario = ?",
        (user_id,),
            )
        retorno = cursor.fetchall()
        if not retorno:
            raise IndexError("genero não encontrada")
        else:
            return retorno

    # Adicione este método na classe Movie do arquivo movie_model.py

@staticmethod  
def get_avaliacoes_usuario(user_id: int):
    """
        get_avaliacoes_usuario - função que retorna todas as avaliações feitas por um usuário específico

        :params user_id: id do usuário para buscar suas avaliações (INTEGER)

        :return: retorna todas as avaliações do usuário com informações básicas do filme
    """
    if not isinstance(user_id, int):
        raise ValueError("Valor de usuário inválido - deve ser um inteiro")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Query que junta avaliações com informações dos filmes (usando apenas campos que existem)
    query = """
        SELECT a.id_avaliacao, a.id_usuario, a.id_filme_tmdb, a.nota, 
               a.comentario, a.data_avaliacao, f.nome as titulo_filme
        FROM avaliacoes a
        JOIN filmes f ON a.id_filme_tmdb = f.id_filme_tmdb
        WHERE a.id_usuario = ?
        ORDER BY a.data_avaliacao DESC
    """
    
    cursor.execute(query, (user_id,))
    retorno = cursor.fetchall()
    
    if not retorno:
        raise IndexError("Nenhuma avaliação encontrada para este usuário")
    else:
        return retorno


if __name__ == '__main__':
    linhas = Movie.put_preference('1','1234')
    print(linhas)


