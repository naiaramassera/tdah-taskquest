from datetime import datetime, timedelta
from backend.models.user_combo import UserCombo

# Janela de 2 horas para manter o combo
COMBO_WINDOW_HOURS = 2

# Thresholds e multiplicadores de moedas
COMBO_TIERS = [
    (10, 3.0, "🔥🔥🔥 ULTRA COMBO!"),
    (5,  2.0, "🔥🔥 MEGA COMBO!"),
    (3,  1.5, "🔥 COMBO!"),
]


def update_combo(user, db) -> dict:
    """Atualiza o combo do usuário e retorna info do combo atual."""
    now = datetime.utcnow()

    combo = db.query(UserCombo).filter_by(user_id=user.id).first()
    if not combo:
        combo = UserCombo(user_id=user.id, combo_count=0, last_task_at=None)
        db.add(combo)

    # Verifica se ainda está dentro da janela
    if combo.last_task_at and (now - combo.last_task_at) <= timedelta(hours=COMBO_WINDOW_HOURS):
        combo.combo_count += 1
    else:
        combo.combo_count = 1  # resetar

    combo.last_task_at = now
    db.commit()

    multiplier, label = get_combo_multiplier(combo.combo_count)
    return {
        "combo_count": combo.combo_count,
        "multiplier": multiplier,
        "label": label,
        "is_combo": combo.combo_count >= 3,
    }


def get_combo_multiplier(combo_count: int) -> tuple[float, str]:
    for threshold, mult, label in COMBO_TIERS:
        if combo_count >= threshold:
            return mult, label
    return 1.0, ""


def get_current_combo(user, db) -> dict:
    combo = db.query(UserCombo).filter_by(user_id=user.id).first()
    if not combo:
        return {"combo_count": 0, "multiplier": 1.0, "label": "", "is_combo": False}

    now = datetime.utcnow()
    if combo.last_task_at and (now - combo.last_task_at) <= timedelta(hours=COMBO_WINDOW_HOURS):
        mult, label = get_combo_multiplier(combo.combo_count)
        return {
            "combo_count": combo.combo_count,
            "multiplier": mult,
            "label": label,
            "is_combo": combo.combo_count >= 3,
        }
    return {"combo_count": 0, "multiplier": 1.0, "label": "", "is_combo": False}
