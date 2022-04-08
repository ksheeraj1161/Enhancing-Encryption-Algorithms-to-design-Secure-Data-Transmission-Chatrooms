import random
import pandas as pd

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = (int)(temp_phi/e)
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def generate_keypair(p, q, r):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
  
    n = p * q * r

    phi = (p-1) * (q-1) * (r-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)    
        
    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n), phi)

def encrypt(plaintext):
    data1 = pd.read_csv("data1.csv") 
    data2 = pd.read_csv("data2.csv")

    key = int(data2['0'][1])
    n = int(data1['0'][3])

    cipher = [(ord(char) ** int(key)) % n for char in plaintext]
    return cipher

def decrypt(ciphertext):
    data1 = pd.read_csv("data1.csv")
    data2 = pd.read_csv("data2.csv")

    key = int(data2['0'][2]) # d
    n = int(data1['0'][3])

    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)
    

if __name__ == '__main__':

    print("\n\nModified RSA Encrypter/ Decrypter")

    primes=[]
    total_no_primes = 0
    with open('primes.txt') as pfile:
        for line in pfile:
            primes.append(int(line)) 
            total_no_primes += 1
    p = primes[random.randint(1, total_no_primes-1)]
    q = primes[random.randint(1, total_no_primes-1)]
    r = primes[random.randint(1, total_no_primes-1)]


    print("Generating your public/private keypairs now . . .")
    public, private, phi = generate_keypair(p, q, r)
    print("\nYour public key is ", public ," and your private key is ", private)

    data1 = [p, q, phi, public[1]] 
    df = pd.DataFrame(data1)
    df.to_csv('data1.csv') 

    data2 = [r, public[0], private[0]]
    df = pd.DataFrame(data2)
    df.to_csv('data2.csv')

    message = input("\nEnter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(message)
    print("\nYour encrypted message is: ")
    print(''.join([str(x) for x in encrypted_msg]))
    print("\nDecrypting message with private key ", private ," . . .")
    print("\nYour message is:")
    print(decrypt(encrypted_msg))
