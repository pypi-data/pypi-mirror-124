from energytt_platform.encrypt import aes256_encrypt, aes256_decrypt


def test__aes256__should_encrypt_and_decrypt_correctly():

    # -- Arrange -------------------------------------------------------------

    key = 'This is my encryption key'
    data = 'This is the string i want encrypted'

    # -- Act -----------------------------------------------------------------

    data_encrypted = aes256_encrypt(
        data=data,
        key=key,
    )

    data_decrypted = aes256_decrypt(
        data_encrypted=data_encrypted,
        key=key,
    )

    # -- Assert --------------------------------------------------------------

    assert data_decrypted == data
    assert data_decrypted != data_encrypted
