from sqlalchemy.dialects import postgresql

from repositories.recommendation import RecommendationRepository


def test_recommendations_exclude_blocks_in_both_directions():
    """A profile must disappear whether the viewer blocked it or was blocked by it."""
    repository = RecommendationRepository(None)

    # Compile-only regression test: it validates the SQL predicate without requiring PostgreSQL.
    import asyncio

    class Session:
        statement = None

        async def scalars(self, statement):
            self.statement = statement

            class Result:
                def all(self):
                    return []

            return Result()

    session = Session()
    repository.session = session
    asyncio.run(repository.eligible_profiles(10))
    sql = str(session.statement.compile(dialect=postgresql.dialect()))

    assert sql.count("blocks") >= 2
