# deephaven-aws-public-blockchain

This is an example of using [Deephaven](https://github.com/deephaven/deephaven-core) to navigate the [AWS Public Blockchain](https://registry.opendata.aws/aws-public-blockchain/) using Deephaven S3 support.

## Run

Clone this repository and run:

```bash
docker compose up -d --build
```

Navigate to http://localhost:10000 and open up the `transactions` table or `transactions_by_date` partitioned table.

## TLS

See the [tls](https://github.com/devinrsmith/deephaven-aws-public-blockchain/tree/tls) branch for a more secure, TLS-based configuration.
