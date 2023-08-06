from azure.kusto.data import KustoClient, KustoConnectionStringBuilder


def create_query_engine(cluster):

    client_id = dbutils.secrets.get(scope="ce5", key="adxClientId")
    client_secret = dbutils.secrets.get(scope="ce5", key="adxClientSecret")
    cluster_name = dbutils.secrets.get(scope="ce5", key="adxClusterName")
    tenant_id = dbutils.secrets.get(scope="ce5", key="adxTenantId")

    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(cluster, client_id, client_secret, tenant_id)

    return KustoClient(kcsb)