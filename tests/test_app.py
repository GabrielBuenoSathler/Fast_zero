from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


from dataclasses import asdict           
                                         
from sqlalchemy import select            
                                         
from fast_zero.models import User,Book      

def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert





def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'books':[]
    }
def test_create_book(session, mock_db_time):
    with mock_db_time(model=Book):
        book = Book(
            book_name='Test Book',
            book_description='Test Book Description',
            user_id=1,  # Assume que o 'user' já existe
            )

    # Adiciona o livro à sessão assíncrona
        session.add(book)
        session.commit()  # Commit assíncrono



    # Buscando o livro inserido
        result =  session.execute(select(Book).where(Book.book_name == 'Test Book'))
        book_from_db = result.scalar_one()  # Obtém o único resultado

    # Asserção
        assert book_from_db.book_name == 'Test Book'
        assert book_from_db.book_description == 'Test Book Description'
        assert book_from_db.user_id == 1
        



