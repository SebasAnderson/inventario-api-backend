"""Initial schema with all 6 tables from ERD

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-11-16 15:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Catálogo y Clasificación
    op.create_table(
        'franquicias',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_franquicias_id'), 'franquicias', ['id'], unique=False)
    op.create_index(op.f('ix_franquicias_nombre'), 'franquicias', ['nombre'], unique=True)

    op.create_table(
        'editoriales',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_editoriales_id'), 'editoriales', ['id'], unique=False)
    op.create_index(op.f('ix_editoriales_nombre'), 'editoriales', ['nombre'], unique=True)

    op.create_table(
        'demografias',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_demografias_id'), 'demografias', ['id'], unique=False)
    op.create_index(op.f('ix_demografias_nombre'), 'demografias', ['nombre'], unique=True)

    # 2. Usuarios y Seguridad
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('rol', sa.String(length=50), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)

    # 3. Productos (Catálogo)
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('titulo_nombre', sa.String(length=255), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('precio_venta', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock_actual', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tipo_producto', sa.String(length=50), nullable=False),
        sa.Column('id_franquicia', sa.Integer(), nullable=False),
        sa.Column('numero_tomo', sa.String(length=50), nullable=True),
        sa.Column('id_editorial', sa.Integer(), nullable=True),
        sa.Column('id_demografia', sa.Integer(), nullable=True),
        sa.Column('isbn', sa.String(length=20), nullable=True),
        sa.Column('marca_fabricante', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['id_demografia'], ['demografias.id'], ),
        sa.ForeignKeyConstraint(['id_editorial'], ['editoriales.id'], ),
        sa.ForeignKeyConstraint(['id_franquicia'], ['franquicias.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isbn')
    )
    op.create_index(op.f('ix_productos_id'), 'productos', ['id'], unique=False)
    op.create_index(op.f('ix_productos_titulo_nombre'), 'productos', ['titulo_nombre'], unique=False)
    op.create_index(op.f('ix_productos_tipo_producto'), 'productos', ['tipo_producto'], unique=False)
    op.create_index(op.f('ix_productos_isbn'), 'productos', ['isbn'], unique=True)

    # 4. Operatividad y Auditoría (Movimientos de Stock)
    op.create_table(
        'movimientos_stock',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_producto', sa.Integer(), nullable=False),
        sa.Column('id_usuario', sa.Integer(), nullable=False),
        sa.Column('tipo_movimiento', sa.String(length=50), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('fecha_movimiento', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('cantidad > 0', name='check_cantidad_positiva'),
        sa.ForeignKeyConstraint(['id_producto'], ['productos.id'], ),
        sa.ForeignKeyConstraint(['id_usuario'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movimientos_stock_id'), 'movimientos_stock', ['id'], unique=False)
    op.create_index(op.f('ix_movimientos_stock_id_producto'), 'movimientos_stock', ['id_producto'], unique=False)
    op.create_index(op.f('ix_movimientos_stock_id_usuario'), 'movimientos_stock', ['id_usuario'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_movimientos_stock_id_usuario'), table_name='movimientos_stock')
    op.drop_index(op.f('ix_movimientos_stock_id_producto'), table_name='movimientos_stock')
    op.drop_index(op.f('ix_movimientos_stock_id'), table_name='movimientos_stock')
    op.drop_table('movimientos_stock')

    op.drop_index(op.f('ix_productos_isbn'), table_name='productos')
    op.drop_index(op.f('ix_productos_tipo_producto'), table_name='productos')
    op.drop_index(op.f('ix_productos_titulo_nombre'), table_name='productos')
    op.drop_index(op.f('ix_productos_id'), table_name='productos')
    op.drop_table('productos')

    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_table('usuarios')

    op.drop_index(op.f('ix_demografias_nombre'), table_name='demografias')
    op.drop_index(op.f('ix_demografias_id'), table_name='demografias')
    op.drop_table('demografias')

    op.drop_index(op.f('ix_editoriales_nombre'), table_name='editoriales')
    op.drop_index(op.f('ix_editoriales_id'), table_name='editoriales')
    op.drop_table('editoriales')

    op.drop_index(op.f('ix_franquicias_nombre'), table_name='franquicias')
    op.drop_index(op.f('ix_franquicias_id'), table_name='franquicias')
    op.drop_table('franquicias')
