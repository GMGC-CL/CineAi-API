from flask import Blueprint, request, jsonify,send_from_directory
from api.controllers.movie_controller import Api
from werkzeug.exceptions import HTTPException
movie_routes = Blueprint('movie_routes', __name__)
api = Api()



@movie_routes.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API de filmes online'}), 200

@movie_routes.route('/movies', methods=['GET'])
def get_all_movies():
    try:
        limit_query = request.args.get('limit', default=10, type=int)
        jMovies = api.get_all_movies(limit_query)
        return jsonify(jMovies), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return jsonify({'error': 'Não foi possível encontrar os filmes'}), 500


@movie_routes.route('/genres', methods=['GET'])
def get_all_genres():
    try:
        jGenres = api.get_all_genres()
        return jsonify(jGenres), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Não foi possível encontrar os generos'}), 500

@movie_routes.route('/movies/genre/<string:genre_id>', methods=['GET'])
def get_movie_for_genre(genre_id):
    limit_query = request.args.get('limit', default=10, type=int)
    try:
        jMovies = api.get_movies_for_genre(genre_id, limit_query)
        return jsonify(jMovies), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Não foi possível encontrar os filmes'}), 500

@movie_routes.route('/movies/name/<string:movie_name>', methods=['GET'])
def get_movies_for_name(movie_name):
    try:
        jMovies = api.get_movies_for_name(movie_name)
        return jsonify(jMovies), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Não foi possível encontrar os filmes'}), 500

@movie_routes.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    try:
        jMovie = api.get_movie_by_id(int(movie_id))
        return jsonify(jMovie), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Não foi possível encontrar o filme'}), 500

@movie_routes.route('/movies/<int:movie_id>/similar', methods=['GET'])
def get_consine_movie_by_id(movie_id):
    limit_query = request.args.get('limit', default=10, type=int)
    try:
        jMovie = api.cousine_movies(movie_id,limit_query)
        return jsonify(jMovie), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Não foi possível encontrar o filme'}), 500
    

@movie_routes.route('/movies/<int:filme_id>/avaliar', methods=['POST'])
def registrar_avaliacao(filme_id):
    try:
        data = request.get_json()

        usuario_id = data.get("usuario_id")
        nota = data.get("nota")
        comentario = data.get("comentario")

        if not usuario_id or not nota:
            return jsonify({'error': 'Campos obrigatórios não fornecidos'}), 400

        sucesso = api.registrar_avaliacao(usuario_id, str(filme_id), nota, comentario)

        if sucesso:
            return jsonify({'message': 'Avaliação registrada com sucesso'}), 201
        else:
            return jsonify({'error': 'Erro ao registrar avaliação'}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro no servidor ao registrar avaliação'}), 500
    
    
@movie_routes.route('/movies/<int:movie_id>/avaliacoes', methods=['GET'])
def get_avaliacao(movie_id):
    try:
        avaliacoes = api.get_avaliacao(str(movie_id))
        if avaliacoes:
            return jsonify(avaliacoes), 200
        else:
            return jsonify({'message': 'Nenhuma avaliação encontrada'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro ao buscar avaliações'}), 500
    

@movie_routes.route('/usuarios/registrar', methods=['POST'])
def registrar_usuario():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        nome = data.get('nome')
        if not nome or not email or not senha:
            return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400
        if not isinstance(nome, str):
            return jsonify({'error': 'Nome deve ser uma string'}), 400

        if not email or not senha:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        sucesso = api.registrar_usuario(nome, email, senha)

        if sucesso:
            return jsonify({'message': 'Usuário registrado com sucesso'}), 201
        else:
            return jsonify({'error': f'Erro ao registrar usuário {sucesso}'}), 500

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': e}), 500


@movie_routes.route('/usuarios/login', methods=['POST'])
def autenticar_usuario():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        token = api.autenticar_usuario(email, senha)
        return jsonify(token), 200

    except HTTPException as http_err:
        return jsonify({'error': http_err.detail}), http_err.status_code
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro no servidor ao autenticar usuário'}), 500
