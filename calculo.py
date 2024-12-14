import gmpy2
from Crypto.Util import number

def calculate_totient(p, q):
    return (p - 1) * (q - 1)

# Generate two large prime numbers
p = number.getPrime(2006)
q = number.getPrime(2009)

# Calculate n
n = p * q

# Calculate Euler's Totient function
phi = calculate_totient(p, q)

# Choose an integer e such that 1 < e < phi and gcd(e, phi) = 1; e is the public key exponent
e = 65537

# Calculate d, the modular multiplicative inverse of e (private key exponent)
d = pow(e, -1, phi)

print(f"p: {p}\n")
print(f"q: {q}\n")
print(f"Public key: (n={n}, e={e})\n")
print(f"Private key: (n={n}, d={d})\n")