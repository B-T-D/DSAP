def hash_code(string: str) -> int:
    """Cyclic-shift hash code computation for a character string. Shifts 5 bits
    from start to end."""
    mask = (1 << 32) - 1 # Limit to 32 bit integers.
    h = 0
    for character in string:
        h = (h << 5 & mask)|(h >> 27) # Remove the first 5 bits of string and
                                        # move them to be the last 5 bits.
                                        # 27 is (32 - 5).
        h += ord(character)
    return h
            
