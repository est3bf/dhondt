from sqlalchemy.orm import relationship, validates
from dhondt.db.controller import DB
from sqlalchemy import ForeignKey, Column, DateTime, Integer, String


class ScrutinyTable(DB.Base):
    """Table that contains all scrutiny for each electoral district"""

    __tablename__ = "scrutiny"
    # Columns
    id = Column(Integer, primary_key=True, doc="id of the scrutiny (autogenerated)")

    voting_date = Column(DateTime, nullable=False, doc="date when the voting starts")

    scrutiny_date = Column(DateTime, nullable=False, doc="date when the scrutiny ends")

    district_id = Column(
        Integer,
        ForeignKey("district.id"),
        nullable=False,
        doc="foreign key to the district where the scrutiny takes place",
    )

    seats = Column(
        Integer, nullable=False, doc="Total parliaments seats available in the scrutiny"
    )

    name = Column(String, nullable=False, doc="Name of Scrutiny")

    # Relationships
    district = relationship("DistrictTable", back_populates="scrutiny")
    """Many-to-one: Many scrutinies for one district"""
    dhondtresult = relationship("DhondtResultTable", back_populates="scrutiny")

    def dict(self):
        return {
            "id": self.id,
            "votingDate": self.voting_date,
            "scrutinyDate": self.scrutiny_date,
            "districtId": self.district_id,
            "seats": self.seats,
            "name": self.name,
        }


class DistrictTable(DB.Base):
    """Table that describes the electoral district"""

    __tablename__ = "district"
    # Columns
    id = Column(Integer, primary_key=True, doc="id of the district (autogenerated)")

    name = Column(String, nullable=False, unique=True, doc="the name of the test type")

    # Relationships
    scrutiny = relationship("ScrutinyTable", back_populates="district")
    """Many-to-one: Many scrutinies for one district. Duplicate due to back_populates"""
    politicalpartylist = relationship(
        "PoliticalPartyListTable", back_populates="district"
    )
    """Many-to-one: Many political party list for one district. Duplicate due to back_populates"""

    @validates("name")
    def convert_lower(self, key, value):
        return value.lower()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class PoliticalPartyListTable(DB.Base):
    """Table that describes the political party list"""

    __tablename__ = "politicalpartylist"
    # Columns
    id = Column(
        Integer, primary_key=True, doc="id of the political party list (autogenerated)"
    )

    district_id = Column(
        Integer,
        ForeignKey("district.id"),
        nullable=False,
        doc="foreign key to the district table",
    )

    name = Column(
        String,
        nullable=False,
        unique=True,
        doc="name of the party list (passed as argument)",
    )

    votes = Column(Integer, default=0, doc="quantity of votes received")

    electors = Column(Integer, nullable=False, doc="number of electors in the list")

    # Relationships
    district = relationship("DistrictTable", back_populates="politicalpartylist")
    """Many-to-one: Many political party list for one district"""
    seatspoliticalparties = relationship(
        "SeatsPoliticalPartiesTable", back_populates="politicalpartylist"
    )
    """Many-to-one: Many seat results for one total result"""

    @validates("name")
    def convert_lower(self, key, value):
        return value.lower()

    def dict(self):
        return {
            "id": self.id,
            "districtId": self.district_id,
            "name": self.name,
            "votes": self.votes,
            "electors": self.electors,
        }


class SeatsPoliticalPartiesTable(DB.Base):
    """Table that describes the result of seats for each p.p. list
    using D'hondt method at given time"""

    __tablename__ = "seatspoliticalparties"
    # Columns
    id = Column(
        Integer,
        primary_key=True,
        doc="id of the seats for each political parties (autogenerated)",
    )

    dhondtresult_id = Column(
        Integer,
        ForeignKey("dhondtresult.id"),
        nullable=False,
        doc="foreign key to the dhondtresult table",
    )

    politicalpartylist_id = Column(
        Integer,
        ForeignKey("politicalpartylist.id"),
        nullable=False,
        doc="foreign key to the politicalpartylist table",
    )

    seats = Column(
        Integer, nullable=False, doc="number of seats calculated for p.p. list"
    )

    # Relationships
    politicalpartylist = relationship(
        "PoliticalPartyListTable", back_populates="seatspoliticalparties"
    )
    """Many-to-one: Many seats results for one p.p. list"""
    dhondtresult = relationship(
        "DhondtResultTable",
        foreign_keys=[dhondtresult_id],
        back_populates="seatspoliticalparties",
    )
    """Many-to-one: Many seat results for one total result"""

    def dict(self):
        return {
            "pplistId": self.politicalpartylist_id,
            "seats": self.seats,
            "pplistName": self.politicalpartylist.name,
        }


class DhondtResultTable(DB.Base):
    """Table that describes the result of seats using D'hondt method at given time"""

    __tablename__ = "dhondtresult"
    # Columns
    id = Column(
        Integer, primary_key=True, doc="id of the dhondt result (autogenerated)"
    )

    scrutiny_id = Column(
        Integer,
        ForeignKey("scrutiny.id"),
        nullable=False,
        doc="foreign key to the scrutiny table",
    )

    result_date = Column(
        DateTime, nullable=False, doc="date when the D'Hondt method is performed"
    )

    # Relationships
    scrutiny = relationship("ScrutinyTable", back_populates="dhondtresult")
    """Many-to-one: Many results for one scrutiny"""
    seatspoliticalparties = relationship(
        "SeatsPoliticalPartiesTable", back_populates="dhondtresult"
    )
    """Many-to-one: Many seat results for one total result"""

    def dict(self):
        return {
            "resultId": self.id,
            "districtId": self.scrutiny.district_id,
            "scrutinyId": self.scrutiny_id,
            "scrutinyName": self.scrutiny.name,
            "calculationDate": self.result_date,
            "seatsResults": [x.dict() for x in self.seatspoliticalparties],
        }
