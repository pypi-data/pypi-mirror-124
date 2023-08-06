from azure.kusto.data import KustoClient, KustoConnectionStringBuilder


def create_engine(cluster, client_id, client_secret, tenant_id):

    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(cluster,
                                                                                client_id,
                                                                                client_secret,
                                                                                tenant_id)

    return KustoClient(kcsb)
