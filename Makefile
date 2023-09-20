API_KEY=
SECRET_KEY=
CA_PATH=
CA_PASSWD=
PERSON_ID=

STOCK_ID=0050
FROM=2023-01-01
TO=2023-01-31
OUTPUT=output.csv

all:
	python3 index.py \
		--sandbox \
		--api-key $(API_KEY) \
		--secret-key $(SECRET_KEY) \
		--ca-path $(CA_PATH) \
		--ca-passwd $(CA_PASSWD) \
		--person-id $(PERSON_ID) \
		--stock-id $(STOCK_ID) \
		--from-date $(FROM) \
		--to-date $(TO) \
		--output $(OUTPUT)
