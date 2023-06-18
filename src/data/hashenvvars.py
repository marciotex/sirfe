# por ora não usando hash
# reavaliar no futuro
# segurança
import hashlib

original_value = 'cole aqui o valor exato, entre as aspas'
hashed_value = hashlib.sha256(original_value.encode()).hexdigest()

print (f'Valor original: {original_value}')
print(f'Valor hash: {hashed_value}')

# valor acessado em Gerar link, na aba exportações
# valor abaixo é mero exemplo, está errado
AUTHORIZATION_HEADER_SME_ORIGINAL = "Basic NDMxsdasassdadasdsadRqsadasdaRlRpU2NXVDl5ZHYy"
AUTHORIZATION_HEADER_SME_HASHED = hashlib.sha256(AUTHORIZATION_HEADER_SME_ORIGINAL.encode()).hexdigest()

print (f'Valor original: {AUTHORIZATION_HEADER_SME_ORIGINAL}')
print(f'Valor hash: {AUTHORIZATION_HEADER_SME_HASHED}')
print('Copie o valor hash para uso e não esqueça de apagar o valor da variável AUTHORIZATION_HEADER_SME_ORIGINAL no script se você quer mantê-la protegida.')