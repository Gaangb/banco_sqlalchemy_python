import sqlalchemy

from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine, inspect, select, func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship( # Link do relacionamento
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


print(User.__tablename__)

# Conexao com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# verifica o squema do banco de dados
insp = inspect(engine)
print(insp.has_table("user_account"))

print(insp.get_table_names())
print(insp.default_schema_name)

with Session(engine) as session:
    gael = User(
        name='Gael',
        fullname='Angelo Gabriel',
        address=[Address(email_address='gaeltec@email.com')]
    )

    izzana = User(
        name='Izzana',
        fullname='Izzana Barbosa',
        address=[Address(email_address='izzaprogramer@email.com'),
                 Address(email_address='zaza@email.com')]
    )

    joao = User(
        name='joao',
        fullname='Joao Gomes'
    )

    # Enviar para o Banco
    session.add_all([gael, izzana, joao])
    session.commit()

stmt = select(User).where(User.name.in_(['Gael'])) # para acessar o dado é necessario usar o for para percorrer
print("Recuperando usuários a partir de condição de filtragem")
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print("\nRecuperando os endereços de email do segundo objeto")
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.fullname.asc())

print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

print("\nRecuperando usuarios que possuem email registrado")
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)

connection = engine.connect() # faz a conexão com o banco
results = connection.execute(stmt_join).fetchall() # retorna tudo
for result in results:
    print(result)

print("\nContando a quantidade de usuarios registrados")
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)
