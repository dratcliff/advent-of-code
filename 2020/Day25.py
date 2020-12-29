import utils


def transform(subj, pub):
    val = 1

    i = 0
    while val != pub:
        i += 1
        val *= subj
        val %= 20201227

    return i


def transform2(subj, loop):
    val = 1

    for i in range(loop):
        val *= subj
        val %= 20201227

    return val


def run(card_pub, door_pub):
    """
    The handshake used by the card and the door involves an operation that transforms a subject number. To transform a subject number, start with the value 1. Then, a number of times called the loop size, perform the following steps:

Set the value to itself multiplied by the subject number.
Set the value to the remainder after dividing the value by 20201227.
The card always uses a specific, secret loop size when it transforms a subject number. The door always uses a different, secret loop size.

The cryptographic handshake works like this:

The card transforms the subject number of 7 according to the card's secret loop size. The result is called the card's public key.
The door transforms the subject number of 7 according to the door's secret loop size. The result is called the door's public key.
The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device. Now, the card has the door's public key, and the door has the card's public key. Because you can eavesdrop on the signal, you have both public keys, but neither device's loop size.
The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
The door transforms the subject number of the card's public key according to the door's loop size. The result is the same encryption key as the card calculated."""

    card_loop = transform(7, card_pub)
    print("card loop", card_loop)
    door_loop = transform(7, door_pub)
    print("door loop", door_loop)
    enc_key = transform2(card_pub, door_loop)
    print("enc key one", enc_key)
    enc_key2 = transform2(door_pub, card_loop)
    print("enc key two", enc_key2)
    assert enc_key == enc_key2


def test_day_twenty_one():
    card_pub = 5764801
    door_pub = 17807724
    run(card_pub, door_pub)


def day_twenty_one():
    card_pub = 8458505
    door_pub = 16050997
    run(card_pub, door_pub)


if __name__ == "__main__":
    day_twenty_one()
