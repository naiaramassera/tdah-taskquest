from backend.models.user_skin import UserSkin
from backend.models.xp import XPProgress

def unlock_level_skins(user, db):
    from backend.models.user_skin import UserSkin
    from backend.models.xp import XPProgress

    xp = db.query(XPProgress).filter_by(user_id=user.id).first()

    if not xp:
        return []

    unlocked_skins = []

    skins = db.query(UserSkin).filter_by(
        user_id=user.id,
        unlock_type="level"
    ).all()

    for skin in skins:
        if not skin.unlocked and xp.level >= skin.unlock_value:
            skin.unlocked = True
            unlocked_skins.append(skin.skin_name)

    db.commit()

    return unlocked_skins


def unlock_achievement_skins():
    return None