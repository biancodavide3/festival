# ATTENZIONE non fa parte dell'applicazione flask in se
# serviva solo a ottenere l'hash della password "password" utilizzata per tutti gli utenti

from werkzeug.security import generate_password_hash

print(generate_password_hash("password", method="scrypt"))