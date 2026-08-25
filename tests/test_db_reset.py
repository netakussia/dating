from utils.db_reset import get_reset_table_names


def test_reset_table_names_are_sorted_for_fk_safe_cleanup() -> None:
    tables = get_reset_table_names()

    assert tables[:3] == ["likes", "dislikes", "matches"]
    assert tables[-2:] == ["profiles", "users"]
    assert "admin_logs" in tables
