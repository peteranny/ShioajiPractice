SANDBOX=${SANDBOX:-1}
API_KEY=${API_KEY}
SECRET_KEY=${SECRET_KEY}
CA_PATH=${CA_PATH:-./Sinopac.pfx}
CA_PASSWD=${CA_PASSWD}
PERSON_ID=${PERSON_ID}
STOCK_ID=${STOCK_ID:-0050}
FROM=${FROM:-2023-01-01}
TO=${TO:-2023-01-31}
ORDER_QUANTITY=${ORDER_QUANTITY:-10}
MA_DAYS=${MA_DAYS:-60}
OUTPUT=${OUTPUT:-output.csv}

if [ -n "$(command -v python3)" ]; then BIN=python3; else BIN=python; fi

$BIN transaction.py \
               $( [ "$SANDBOX" == "0" ] && echo || echo --sandbox) \
               --api-key ${API_KEY} \
               --secret-key ${SECRET_KEY} \
               --ca-path ${CA_PATH} \
               --ca-passwd ${CA_PASSWD} \
               --person-id ${PERSON_ID} \
               --stock-id ${STOCK_ID} \
               --from-date ${FROM} \
               --to-date ${TO} \
               --order-quantity ${ORDER_QUANTITY} \
               --ma-days ${MA_DAYS} \
               --output ${OUTPUT}
