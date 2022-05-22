import random
import os
import genLargePrimes


def Extended_euclid(a, b):
	x0, x1, y0, y1 = 0, 1, 1, 0

	while a != 0:
		q, b, a = b//a, a, b % a
		y0, y1 = y1, y0 - q*y1
		x0, x1 = x1, x0 - q*x1

	return b, x0, y0


def generatePublicKey(totient):
	public_key = random.randrange(3, totient)
	while not genLargePrimes.is_prime(public_key):
		print("Generating public key : ", public_key)
		public_key += 1
	return public_key


def generatePrivateKey(public_key, totient):
	g, _, private_key = Extended_euclid(int(totient), int(public_key))
	if private_key > totient:
		private_key = private_key % totient
	elif private_key < 0:
		private_key += totient
	return private_key


def runRSA(bits):
    p = genLargePrimes.generate_prime_number(bits)
    q = genLargePrimes.generate_prime_number(bits)
    r = genLargePrimes.generate_prime_number(bits)
    s = genLargePrimes.generate_prime_number(bits)
    totient2 = (s-1)*(r-1)
    totient1 = (p-1)*(q-1)
    n = p*q
    z = r*s
    public_key1 = generatePublicKey(totient1)
    public_key2 = generatePublicKey(totient2)
    private_key1 = generatePrivateKey(public_key1, totient1)
    private_key2 = generatePrivateKey(public_key2, totient2)
    return n, z, totient1, totient2, public_key1, private_key1, public_key2, private_key2 ,p,q,r,s


def encrypt(message, public_key1, public_key2, n, z):
    enc_list1 = []
    enc_list2 = []
    #print("Encypting your message..")
    for char in message:
        print(char)
        mess = ord(char)
        enc_mess = str(pow(mess, public_key1, n))
        print(enc_mess)
        enc_list1.append(enc_mess)
        
    for char in enc_list1:
        mess = int(char)
        ciph = str(pow(mess, public_key2, z))
        print(ciph)
        enc_list2.append(ciph)
    return enc_list2

def gcd(p, q): 
	
	if q == 0: 
		return p 
		
	return gcd(q, p % q) 

def lcm(p, q): 
	return p * q / gcd(p, q) 

def egcd(e, phi): 
	
	if e == 0: 
		return (phi, 0, 1) 
	else: 
		g, y, x = egcd(phi % e, e) 
		return (g, x - (phi // e) * y, y) 

def modinv(e, phi): 
	
	g, x, y = egcd(e, phi) 
	return x % phi 


def chineseremaindertheorem(dq, dp, p, q, c): 
	
	# Message part 1 
	m1 = pow(c, dp, p) 
	
	# Message part 2 
	m2 = pow(c, dq, q) 
	
	qinv = modinv(q, p) 
	h = (qinv * (m1 - m2)) % p 
	m = m2 + h * q 
	return m 


def decrypt(ct_list, private_key1,private_key2,p,q,r,s,z):
    
    c1 = []
    decrypted_mess = []
    dq = pow(private_key1, 1, q - 1) 
    dp = pow(private_key1, 1, p - 1)
    print("\nDecrypting your message\n")
    print(ct_list)
    print(type(ct_list))
    print(len(ct_list))
    for ct in ct_list:
        print(ct)
        decr = (pow(int(ct), private_key2, z))
        print(decr)
        c1.append(decr)
    for ct in c1:
        decr = chineseremaindertheorem(dq, dp, p, q, ct)
        print(decr)
        decrypted_mess.append(chr(decr))
        
    return decrypted_mess