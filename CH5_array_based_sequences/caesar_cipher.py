"""DSAP's class-based implementation of Caesar cipher simple encryption
algorithm."""

class CaesarCipher:
    """Class for encrypting and decrypting strings of upper case ASCII
    characters using the Caesar cipher."""

    def __init__(self, shift):
        """Construct Caesar cipher using a given integer shift for rotation
        distance."""
        encoder = [None] * 26 # temp array for encryption
        decoder = [None] * 26 # temp array for decryption
        for k in range(26): # convert the numbers to ints from 0 to 25
            encoder[k] = chr((k + shift) % 26 + ord('A'))
            decoder[k] = chr((k - shift) % 26 + ord('A'))
        self._forward = ''.join(encoder) # will store as string since fixed
        self._backward = ''.join(decoder)

    def encrypt(self, message):
        """REturn string representing encrypted message."""
        return self._transform(message, self._forward)

    def decrypt(self, secret):
        """Return decrypted message given encrypted secret."""
        return self._transform(secret, self._backward)

    def _transform(self, original, code):
        """Utility to perform transformation based on given code string."""
        msg = list(original)
        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord('A') # get the index from 0 to 25
                msg[k] = code[j] # replace this character
        return ''.join(msg)

if __name__ == '__main__':
    cipher = CaesarCipher(shift=3)
    message = "THE EAGLE IS IN PLAY; MEET AT JOE'S."
    coded = cipher.encrypt(message)
    print('Secret: ', coded)
    answer = cipher.decrypt(coded)
    print('Message: ', answer)
