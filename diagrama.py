from api.models import db, User # importa modelos
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData

# Conectar con la metadata de SQLAlchemy
metadata = db.metadata

# Crear el diagrama del esquema
graph = create_schema_graph(
    metadata=metadata,
    show_datatypes=False,  # No mostrar los tipos de datos de las columnas
    show_indexes=False,    # No mostrar índices
    rankdir='LR',          # Dirección del diagrama de izquierda a derecha (opcional)
    concentrate=False      # Evitar que las líneas se unan
)

# Exportar el gráfico a un archivo .jpg
graph.write_jpg('diagrama.jpg')
