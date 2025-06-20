import argon2

TIME_COST_DEFAULT: int = 14
MEMORY_COST_DEFAULT: int = 131072  # 128 MiB
PARALLELISM_DEFAULT: int = 4
HASH_LEN_DEFAULT: int = 32
SALT_LEN_DEFAULT: int = 16


def mib_to_kib(mebi: int):
    """
    Convert mebibytes (MiB) to kibibytes (KiB).

    Args:
        mebi (int): The number of mebibytes to convert.

    Returns:
        kibi (int): The equivalent number of kibibytes.
    """
    kibi = mebi * 1024
    return kibi


def gib_to_kib(gibi: int):
    """
    Convert gibibytes (GiB) to kibibytes (KiB).

    Args:
        gibi (int): The number of gibibytes to convert.

    Returns:
        kibi (int): The equivalent number of kibibytes.
    """
    kibi = gibi * (1024**2)
    return kibi


class Argon2IDHasher:
    def __init__(
        self,
        time_cost: int = TIME_COST_DEFAULT,
        memory_cost: int = MEMORY_COST_DEFAULT,
        parallelism: int = PARALLELISM_DEFAULT,
        hash_len: int = HASH_LEN_DEFAULT,
        salt_len: int = SALT_LEN_DEFAULT,
    ):
        """
        Initialises the Argon2IDHasher with configurable parameters.

        Args:
            time_cost (int): The number of iterations to perform when hashing. Higher values increase computation time and security.
                _Default_: 14 iterations
            memory_cost (int): The amount of memory (in kibibytes) to use during hashing. Higher values increase security.
                _Default_: 128 MiB
            parallelism (int): The number of parallel threads to use for hashing.
                _Default_: 4 threads
            hash_len (int): The desired length of the resulting hash in bytes.
                _Default_: 32 bytes
            salt_len (int): The length of the random salt to use in bytes.
                _Default_: 16 bytes

        Sets up the internal Argon2ID PasswordHasher instance with the specified parameters.
        IT IS HIGHLY RECOMMENDED TO USE THE DEFAULT VALUES FOR SECURITY REASONS.
        """

        if time_cost < TIME_COST_DEFAULT:
            time_cost = TIME_COST_DEFAULT
        if memory_cost < MEMORY_COST_DEFAULT:
            memory_cost = MEMORY_COST_DEFAULT
        if parallelism < 1:
            parallelism = PARALLELISM_DEFAULT
        if hash_len < 16:
            hash_len = HASH_LEN_DEFAULT
        if salt_len < 8:
            salt_len = SALT_LEN_DEFAULT

        self.ph = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
            type=argon2.low_level.Type.ID,
        )

    def hash(self, password: str) -> str:
        """
        Hashes a password using Argon2ID.
        Args:
            password (str): The password to hash.
        Returns:
            str: The hashed password.
        """
        return self.ph.hash(password)

    def verify(self, hash_str: str, password: str) -> bool:
        """
        Verifies if the provided password matches the given Argon2ID hash.
        Args:
            hash_str (str): The Argon2ID hash to verify against.
            password (str): The plaintext password to check.

        Returns:
            bool: True if the password matches the hash, False otherwise.

        Raises:
            argon2.exceptions.VerifyMismatchError: If the password does not match the hash.
        """

        try:
            return self.ph.verify(hash_str, password)
        except argon2.exceptions.VerifyMismatchError:
            return False


if __name__ == "__main__":
    # Example usage
    hasher = Argon2IDHasher()
    hashed = hasher.hash("mysecretpassword")
    print(f"Hashed password: {hashed}")
    print(f"Does the password match?: {hasher.verify(hashed, 'mysecretpassword')}")
