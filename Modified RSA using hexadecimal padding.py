import random

def isPrime(num):
	if num == 2:
		return True
	elif num < 2 or num % 2 == 0:
		return False
	else:
		for n in range(3, int((num**0.5) + 2), 2):
			if num % n == 0:
				return False
		return True
		
def gcd(one, two):
	while two != 0:
		one, two = two, one % two
	return one

def multiplicativeInverse(e, phi):
	t = 0
	newt = 1
	r = phi
	newr = e
	
	while newr > 0:
		quotient = int(r / newr)
		t, newt = newt, (t - quotient*newt)
		r, newr = newr, (r - quotient*newr)
	
	if r > 1:
		print("Cannot be inversed") 
	if t < 0:
		t = t + phi
	return t

def genKeypair():
	p = random.randint(2, 1000)
	while (not isPrime(p)):
		p = random.randint(2, 1000)
	
	q = random.randint(2, 1000)
	while (not (isPrime(q) and p != q)):
		q = random.randint(2, 1000)
	
	n = p * q

	phi = (p - 1) * (q - 1)
	
	e = random.randint(1, phi)
	g = gcd(phi, e)	
	
	while (g != 1):
		e = random.randint(1, phi)
		g = gcd(phi, e)
	
	d = multiplicativeInverse(e, phi)
	
	return ((e, n), (int(d), n))
	
def encrypt(keypair, msg):
	key, n = keypair
	
	encMsg = [pow(ord(c), key, n) for c in msg]
	
	hexStr = ''
	for letter in encMsg:
		hexChar = '{:05x}'.format(letter)
		hexStr = hexStr + hexChar
	
	return hexStr
	
def decrypt(keypair, msg):
	key, n = keypair
	
	encMsg = []
	for i in range(0,len(msg), 5):
		hexStr = msg[i:i+5]
		encMsg.append(int(hexStr,16))
	
	decMsg = [chr(pow(c, key, n)) for c in encMsg]
	
	return ''.join(decMsg)
	
if __name__ == '__main__':
	
	print("Generating RSA keypair...")
	public, private = genKeypair()
	print("Done!")
	
	print("Public Key: ", public)
	print("Private Key: ", private)
	
	message = input("\nEnter a message:  ")
	encMessage = encrypt(public, message)
	print("\nEncrypted message: ", encMessage, "\n")
	
	decMessage = decrypt(private, encMessage)
	print("Decrypted message: ", decMessage, "\n")
	
