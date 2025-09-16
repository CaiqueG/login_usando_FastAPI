from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path

# Garante que a pasta "keys" existe
keys_dir = Path("keys")
keys_dir.mkdir(exist_ok=True)

# Gera a chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Salva a chave privada em keys/private.pem
with open(keys_dir / "private.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Gera a chave pública a partir da privada
public_key = private_key.public_key()

# Salva a chave pública em keys/public.pem
with open(keys_dir / "public.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("✅ Chaves geradas com sucesso em /keys")
