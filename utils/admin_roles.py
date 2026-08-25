from models.user import UserRole


def normalize_admin_role(role: UserRole | str | None) -> UserRole:
    if role is None:
        return UserRole.USER
    if isinstance(role, str):
        try:
            return UserRole(role)
        except ValueError:
            return UserRole.USER
    return role


def resolve_admin_role(
    user_id: int,
    *,
    owner_admin_id: int | None = None,
    admin_ids: set[int] | None = None,
    user_role: UserRole | None = None,
) -> UserRole:
    if user_role is not None:
        return normalize_admin_role(user_role)
    if owner_admin_id is not None and user_id == owner_admin_id:
        return UserRole.OWNER
    if admin_ids and user_id in admin_ids:
        return UserRole.MODERATOR
    return UserRole.USER


def can_manage_admins(role: UserRole) -> bool:
    return role == UserRole.OWNER


def can_review_moderator_decisions(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_access_moderation(role: UserRole) -> bool:
    return role in {
        UserRole.MODERATOR,
        UserRole.HEAD_MODERATOR,
        UserRole.CHIEF_MODERATOR,
        UserRole.OWNER,
        UserRole.ADMIN,
    }


def can_ban(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_override_case(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_release_cases(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_unban(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_unfreeze(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_view_all_profiles(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_view_audit_history(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_override_appeal_assignment(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}
