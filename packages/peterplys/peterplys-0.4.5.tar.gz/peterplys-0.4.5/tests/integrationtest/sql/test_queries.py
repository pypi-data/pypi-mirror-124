import pytest
from sqlalchemy import orm, exc

from energytt_platform.sql import SqlQuery

from .db import db
from .models import DbTestModel


# -- Helpers -----------------------------------------------------------------


class TestModelQuery(SqlQuery):
    """
    Query DbTestModel.
    """
    def _get_base_query(self) -> orm.Query:
        return self.session.query(DbTestModel)


# -- Fixtures ----------------------------------------------------------------


@pytest.fixture(scope='function')
def seeded_session(session: db.Session):
    """
    TODO
    """
    session.begin()

    try:
        session.add(DbTestModel(string_field='s1', integer_field=1))
        session.add(DbTestModel(string_field='s1', integer_field=2))
        session.add(DbTestModel(string_field='s2', integer_field=1))
        session.add(DbTestModel(string_field='s2', integer_field=2))
    except:
        session.rollback()
    else:
        session.commit()

    yield session


# -- Tests -------------------------------------------------------------------


class TestQueries:
    """
    TODO
    """

    # -- filter() ------------------------------------------------------------

    def test__filter__no_results_exists__should_apply_filter_and_return_nothing(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == 'FOO-BAR')

        count = query.count()
        results = query.all()

        # -- Assert ----------------------------------------------------------

        assert count == 0
        assert len(results) == 0

    @pytest.mark.parametrize('value', ['s1', 's2'])
    def test__filter__results_exists__should_apply_filter_and_return_correct_results(
            self,
            value: str,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == value)

        count = query.count()
        results = query.all()

        # -- Assert ----------------------------------------------------------

        assert count == 2
        assert len(results) == 2
        assert all(result.string_field == value for result in results)

    # -- filter_by() ---------------------------------------------------------

    def test__filter_by__no_results_exists__should_apply_filter_and_return_nothing(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter_by(string_field='FOO-BAR')

        count = query.count()
        results = query.all()

        # -- Assert ----------------------------------------------------------

        assert count == 0
        assert len(results) == 0

    @pytest.mark.parametrize('value', ['s1', 's2'])
    def test__filter_by__results_exists__should_apply_filter_and_return_correct_results(
            self,
            value: str,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter_by(string_field=value)

        count = query.count()
        results = query.all()

        # -- Assert ----------------------------------------------------------

        assert count == 2
        assert len(results) == 2
        assert all(result.string_field == value for result in results)

    # -- one() ---------------------------------------------------------------

    def test__one__one_result__should_return_correct_result(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == 's1') \
            .filter(DbTestModel.integer_field == 1)

        count = query.count()
        result = query.one()

        # -- Assert ----------------------------------------------------------

        assert count == 1
        assert result.string_field == 's1'
        assert result.integer_field == 1

    def test__one__no_results__should_raise_no_result_error(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act + Assert ----------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == 's1') \
            .filter(DbTestModel.integer_field == 9999)

        with pytest.raises(exc.NoResultFound):
            query.one()

        assert query.count() == 0

    # -- one_or_none() -------------------------------------------------------

    def test__one_or_none__one_result__should_return_correct_result(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == 's1') \
            .filter(DbTestModel.integer_field == 1)

        count = query.count()
        result = query.one_or_none()

        # -- Assert ----------------------------------------------------------

        assert count == 1
        assert result.string_field == 's1'
        assert result.integer_field == 1

    def test__one_or_none__no_results__should_return_none(
            self,
            seeded_session: db.Session,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        query = TestModelQuery(seeded_session) \
            .filter(DbTestModel.string_field == 's1') \
            .filter(DbTestModel.integer_field == 9999)

        count = query.count()
        result = query.one_or_none()

        # -- Assert ----------------------------------------------------------

        assert count == 0
        assert result is None

    # -- get() ---------------------------------------------------------------

    # def test__get__one_result__should_return_correct_field(
    #         self,
    #         seeded_session: db.Session,
    # ):
    #     """
    #     TODO
    #     """
    #
    #     # -- Act -------------------------------------------------------------
    #
    #     q = TestModelQuery(seeded_session) \
    #         .filter(DbTestModel.string_field == 's1') \
    #         .filter(DbTestModel.integer_field == 1) \
    #         .only(DbTestModel.string_field)
    #
    #     result = TestModelQuery(seeded_session) \
    #         .filter(DbTestModel.string_field == 's1') \
    #         .filter(DbTestModel.integer_field == 1) \
    #         .get(DbTestModel.string_field)
    #
    #     # -- Assert ----------------------------------------------------------
    #
    #     assert result.string_field == 's1'

    # def test__get__no_results__should_return_none(
    #         self,
    #         seeded_session: db.Session,
    # ):
    #     """
    #     TODO
    #     """
    #
    #     # -- Act + Assert ----------------------------------------------------
    #
    #     query = TestModelQuery(seeded_session) \
    #         .filter(DbTestModel.string_field == 's1') \
    #         .filter(DbTestModel.integer_field == 9999)
    #
    #     count = query.count()
    #     result = query.one_or_none()
    #
    #     assert count == 0
    #     assert result is None
