# coding: utf-8
from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, NVARCHAR, Numeric, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Artist(Base):
    __tablename__ = 'artists'

    ArtistId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(120))


class Employee(Base):
    __tablename__ = 'employees'

    EmployeeId = Column(Integer, primary_key=True)
    LastName = Column(NVARCHAR(20), nullable=False)
    FirstName = Column(NVARCHAR(20), nullable=False)
    Title = Column(NVARCHAR(30))
    ReportsTo = Column(ForeignKey('employees.EmployeeId'), index=True)
    BirthDate = Column(DateTime)
    HireDate = Column(DateTime)
    Address = Column(NVARCHAR(70))
    City = Column(NVARCHAR(40))
    State = Column(NVARCHAR(40))
    Country = Column(NVARCHAR(40))
    PostalCode = Column(NVARCHAR(10))
    Phone = Column(NVARCHAR(24))
    Fax = Column(NVARCHAR(24))
    Email = Column(NVARCHAR(60))

    parent = relationship('Employee', remote_side=[EmployeeId])


class Genre(Base):
    __tablename__ = 'genres'

    Id = Column("GenreId", Integer, primary_key=True)
    Name = Column(NVARCHAR(120))


class MediaType(Base):
    __tablename__ = 'media_types'

    MediaTypeId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(120))


class Playlist(Base):
    __tablename__ = 'playlists'

    PlaylistId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(120))

    tracks = relationship('Track', secondary='playlist_track')


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


t_sqlite_stat1 = Table(
    'sqlite_stat1', metadata,
    Column('tbl', NullType),
    Column('idx', NullType),
    Column('stat', NullType)
)


class Album(Base):
    __tablename__ = 'albums'

    AlbumId = Column(Integer, primary_key=True)
    Title = Column(NVARCHAR(160), nullable=False)
    ArtistId = Column(
        ForeignKey('artists.ArtistId'),
        nullable=False,
        index=True
    )

    artist = relationship('Artist')


class Customer(Base):
    __tablename__ = 'customers'

    CustomerId = Column(Integer, primary_key=True)
    FirstName = Column(NVARCHAR(40), nullable=False)
    LastName = Column(NVARCHAR(20), nullable=False)
    Company = Column(NVARCHAR(80))
    Address = Column(NVARCHAR(70))
    City = Column(NVARCHAR(40))
    State = Column(NVARCHAR(40))
    Country = Column(NVARCHAR(40))
    PostalCode = Column(NVARCHAR(10))
    Phone = Column(NVARCHAR(24))
    Fax = Column(NVARCHAR(24))
    Email = Column(NVARCHAR(60), nullable=False)
    SupportRepId = Column(ForeignKey('employees.EmployeeId'), index=True)

    employee = relationship('Employee')


class Invoice(Base):
    __tablename__ = 'invoices'

    InvoiceId = Column(Integer, primary_key=True)
    CustomerId = Column(
        ForeignKey('customers.CustomerId'),
        nullable=False,
        index=True
    )
    InvoiceDate = Column(DateTime, nullable=False)
    BillingAddress = Column(NVARCHAR(70))
    BillingCity = Column(NVARCHAR(40))
    BillingState = Column(NVARCHAR(40))
    BillingCountry = Column(NVARCHAR(40))
    BillingPostalCode = Column(NVARCHAR(10))
    Total = Column(Numeric(10, 2), nullable=False)

    customer = relationship('Customer')


class Track(Base):
    __tablename__ = 'tracks'

    TrackId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(200), nullable=False)
    AlbumId = Column(ForeignKey('albums.AlbumId'), index=True)
    MediaTypeId = Column(
        ForeignKey('media_types.MediaTypeId'),
        nullable=False,
        index=True
    )
    GenreId = Column(ForeignKey('genres.GenreId'), index=True)
    Composer = Column(NVARCHAR(220))
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)

    album = relationship('Album')
    genre = relationship('Genre')
    media_type = relationship('MediaType')


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    InvoiceLineId = Column(Integer, primary_key=True)
    InvoiceId = Column(
        ForeignKey('invoices.InvoiceId'),
        nullable=False,
        index=True
    )
    TrackId = Column(ForeignKey('tracks.TrackId'), nullable=False, index=True)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Quantity = Column(Integer, nullable=False)

    invoice = relationship('Invoice')
    track = relationship('Track')


t_playlist_track = Table(
    'playlist_track', metadata,
    Column(
        'PlaylistId',
        ForeignKey('playlists.PlaylistId'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'TrackId',
        ForeignKey('tracks.TrackId'),
        primary_key=True,
        nullable=False,
        index=True
    )
)
