import hashlib
import time

def findNonce(dataToHash, bitsToBeZero):
    '''
    A função busca o nonce que gera hash com bits iniciais zerados
    - dataToHash: dados do hash
    - bitsToBeZero: quantidade de bits zero no início
    Inicia contagem de tempo e nonce
    '''
    tempo_inicial = time.time()
    nonce = 0

    # Loop até encontrar nonce válido
    while True:
        nonce_bytes = nonce.to_bytes(4, byteorder='big')
        data_e_nonce = nonce_bytes + dataToHash
        hash_resultado = hashlib.sha256(data_e_nonce).digest()

        if check_leading_zeros(hash_resultado, bitsToBeZero):
            tempo_final = time.time()

            return nonce, tempo_final - tempo_inicial
        nonce += 1

def check_leading_zeros(hash_bytes, bitsToBeZero):
    '''
    hash_bytes: hash gerado
    bitsToBeZero: quantidade de bits zero no início
    A função verifica se o hash tem os bits iniciais zerados
    '''
    total_zero_bits = 0

    # Percorre cada byte do hash
    for byte in hash_bytes:
        if total_zero_bits >= bitsToBeZero:
            break

        binario = format(byte, '08b')

        # Verifica bit a bit se é zero
        for bit in binario:
            if bit == '1':
                return False  
            total_zero_bits += 1
            
            if total_zero_bits >= bitsToBeZero:
                return True  

    return True  