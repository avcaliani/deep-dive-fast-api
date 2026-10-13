from app import security

PASSLIB_HASH = "$2b$12$YPTegCKiJ0deDBeupkq1XuLFKxeMyVUp.TMtGGM8QbwV18DgXIxk2"  # pragma: allowlist secret


def test_hash_password_is_bcrypt_and_not_plain():
    hashed = security.hash_password("schrute-bucks")

    assert hashed.startswith("$2b$")
    assert "schrute-bucks" not in hashed


def test_check_password_accepts_the_right_password():
    hashed = security.hash_password("schrute-bucks")

    assert security.check_password("schrute-bucks", hashed)


def test_check_password_rejects_a_wrong_password():
    hashed = security.hash_password("schrute-bucks")

    assert not security.check_password("beets", hashed)


def test_check_password_accepts_a_hash_made_by_passlib():
    assert security.check_password("schrute-bucks", PASSLIB_HASH)
