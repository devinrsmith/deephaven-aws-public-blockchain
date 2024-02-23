# deephaven-aws-public-blockchain

This is an example of using [Deephaven UI](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui/examples) to navigate the [AWS Public Blockchain](https://registry.opendata.aws/aws-public-blockchain/) using Deephaven S3 support.

## Run

Clone this repository and run:

```bash
docker compose up -d --build
```

Navigate to https://localhost:8443 and open up the `transactions` component. You will likely need to accept the self-signed certificates. Note: these certificates are meant for development purposes only. For more information, see [deephaven-core dev-certs](https://github.com/deephaven/deephaven-core/tree/main/server/dev-certs).

## TLS

See the [tls](https://github.com/devinrsmith/deephaven-aws-public-blockchain/tree/tls) branch for a more secure, TLS-based configuration.
