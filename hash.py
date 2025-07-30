# ATTENZIONE non fa parte dell'applicazione flask in se
# permette di ottenere l'hash di una password con lo stesso algoritmo utilizzato dall'applicatione

from werkzeug.security import generate_password_hash

print(generate_password_hash("password", method="scrypt"))