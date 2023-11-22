# CuentasClarasConservanAmistades

#### MAIN APIS
* /api/v1/beer/ : List all beers, also create, update and delete
* /api/v1/order/ : Create a new Order. Recieve as param a dic of usenames with a dic of beers wih the amount example: {"ivan": {"red":4, "ipa":3},"pedro": {"blonde":1}}
* /api/v1/order/{ID}/get_account/: Get the account for a order by ID, return the detail for each user and the total amount to pay.
* /api/v1/order/payment/equals/: Pay the account, the total amount is divided in equally for each user.
* /api/v1/order/payment/by_consume/: Pay the account, each user pays for what they consume.

# Run on local machine
#### Prerequisites
* Install docker an docker compose: https://docs.docker.com/compose/install/ 

* You must create a .env file on /docker/ There is an example.env.

#### Run the next command to run the projects on your local machine:

* docker-compose up

* Then you can access to http://localhost

#### Run tests:
sh runtests.sh
