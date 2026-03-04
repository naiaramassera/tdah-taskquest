from backend.models.user_wallet import UserWallet

def add_coins(user, amount, db):
    wallet = db.query(UserWallet).filter_by(user_id=user.id).first()

    if not wallet:
        wallet = UserWallet(user_id=user.id, coins=0)
        db.add(wallet)

    wallet.coins += amount
    db.commit()

    return wallet.coins