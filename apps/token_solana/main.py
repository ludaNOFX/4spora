from theblockchainapi import SolanaAPIResource, SolanaCurrencyUnit, SolanaNetwork, SolanaWallet, DerivationPath

MY_API_KEY_ID = 'ключи можно получить здесь https://dashboard.blockchainapi.com/'
MY_API_SECRET_KEY = ''


BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
    api_key_id=MY_API_KEY_ID,
    api_secret_key=MY_API_SECRET_KEY,
)


def example():
    try:
        assert MY_API_KEY_ID is not None
        assert MY_API_SECRET_KEY is not None
    except AssertionError:
        raise Exception("Fill in your key ID pair!")

    # Create a wallet
    secret_recovery_phrase = BLOCKCHAIN_API_RESOURCE.generate_secret_key()
    wallet = SolanaWallet(
        secret_recovery_phrase=secret_recovery_phrase,
        derivation_path=DerivationPath.CLI_PATH,
        passphrase=str(),
        private_key=None,
        b58_private_key=None
    )
    public_key = BLOCKCHAIN_API_RESOURCE.derive_public_key(wallet=wallet)
    print(f"Public Key: {public_key}")
    print(f"Secret Recovery Phrase: {secret_recovery_phrase}")

    BLOCKCHAIN_API_RESOURCE.get_airdrop(public_key)

    def get_balance():
        balance_result = BLOCKCHAIN_API_RESOURCE.get_balance(
            public_key=public_key,
            unit=SolanaCurrencyUnit.SOL,
            network=SolanaNetwork.MAINNET_BETA  
        )
        print(f"Balance: {balance_result['balance']}")

    get_balance()

    airdrop_amount = 0.015
    transfer_fee = 0.000005

    amount_to_send = str(airdrop_amount - transfer_fee)

    transfer_to = "id кошелька"

    transaction_signature = BLOCKCHAIN_API_RESOURCE.transfer(
        wallet=wallet,
        recipient_address=transfer_to,
        amount=amount_to_send,
        network=SolanaNetwork.DEVNET,
        wait_for_confirmation=True
    )

    print("Transferred!")
    print(f"You can view the transaction here: https://explorer.solana.com/tx/{transaction_signature}?cluster=devnet")

    get_balance()


if __name__ == '__main__':
    example()