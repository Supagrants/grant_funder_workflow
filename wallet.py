#wallet transaction code 


from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.message import Message
from solders.hash import Hash
from solana.rpc.api import Client
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer, TransferParams, get_associated_token_address, create_associated_token_account
import base58
import os
from dotenv import load_dotenv
load_dotenv()

# Constants
USDC_MINT = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
client = Client("https://api.devnet.solana.com")


def create_solana_transaction(sender_address_str, recipient_address_str, amount):
    """
    Creates a Solana transaction to transfer USDC tokens.

    Args:
        sender_address_str (str): The sender's public key as a string.
        recipient_address_str (str): The recipient's public key as a string.
        amount (int): The amount of USDC tokens to transfer (in smallest units, 6 decimals).

    Returns:
        str: The base58 encoded serialized transaction string, or None if an error occurred
    """
    try:
        sender_address = Pubkey.from_string(sender_address_str)
        recipient_address = Pubkey.from_string(recipient_address_str)

        # Get token accounts
        sender_token_account = get_associated_token_address(sender_address, USDC_MINT)
        recipient_token_account = get_associated_token_address(recipient_address, USDC_MINT)
        recipient_account_info = client.get_account_info(recipient_token_account)

        instructions = []
        if not recipient_account_info.value:
            # Add create associated token account instruction if needed
            instructions.append(
                create_associated_token_account(
                    payer=sender_address,
                    owner=recipient_address,
                    mint=USDC_MINT
                )
            )

        # Add transfer instruction
        transfer_instruction = transfer(TransferParams(
            program_id=TOKEN_PROGRAM_ID,
            source=sender_token_account,
            dest=recipient_token_account,
            owner=sender_address,
            amount=amount,
            signers=[],
        ))
        instructions.append(transfer_instruction)


        # Create message
        message = Message.new_with_blockhash(
            instructions,
            Pubkey.from_string("11111111111111111111111111111112"),  # System program ID for blockhash
             Hash.from_string("11111111111111111111111111111111") # Use a dummy hash

        )

        # Create transaction
        transaction = Transaction.new_unsigned(message)

        # Serialize and encode transaction
        serialized_transaction = bytes(transaction)
        serialized_transaction_str = base58.b58encode(serialized_transaction).decode('ascii')

        # Create a beautiful message
        message = (
            #f"Transaction ID: {serialized_transaction_str}\n"
            f" TRANSACTION INITIATED "
            f"Sender Address: {sender_address_str}\n"
            f"Receiver Address: {recipient_address_str}\n"
            f"Amount: {amount / 10**6} USDC"  # Convert to human-readable format
        )
        #print(message)  # Print the message or return it as needed

        return message

    except Exception as e:
        print(f"Error creating transaction: {e}")
        return None



