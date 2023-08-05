# from typing import List
# from sqlalchemy import orm, asc, desc, and_
#
# from energytt_platform.sql import SqlQuery
# from energytt_platform.models.meteringpoints import MeteringPointType
#
# from .models import (
#     MeteringPointFilters,
#     MeteringPointOrdering,
#     MeteringPointOrderingKeys,
#     DbMeteringPoint,
#     DbMeteringPointTechnology,
#     DbMeteringPointAddress,
#     DbMeteringPointDelegate,
#     DbTechnology,
# )
#
#
# # -- MeteringPoints ----------------------------------------------------------
#
#
# class MeteringPointQuery(SqlQuery):
#     """
#     Query DbMeteringPoint.
#     """
#     def _get_base_query(self) -> orm.Query:
#         return self.session.query(DbMeteringPoint)
