from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient


def create_engine(cluster, client_id, client_secret, tenant_id):

    # Create ingest uri
    ingest_uri = cluster.split('//')
    ingest_uri.insert(1, '//ingest-')
    ingest_uri = ''.join(ingest_uri)

    # Create connection with string builder
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(ingest_uri,
                                                                                client_id,
                                                                                client_secret,
                                                                                tenant_id)

    return QueuedIngestClient(kcsb)
