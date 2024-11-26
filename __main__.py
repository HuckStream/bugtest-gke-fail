import pulumi
import pulumi_gcp as gcp

# Get configuration values
config = pulumi.Config()
namespace = config.require("namespace")
environment = config.require("environment")
name = config.require("name")

# Create the base resource name
resource_name = f"{namespace}-{environment}-{name}"

# Create a first GKE cluster as usual
cluster1 = gcp.container.Cluster(
    f"{resource_name}-1",
    name=f"{resource_name}-1",
    description="GKE Cluster for testing Pulumi failure mode",
    initial_node_count=2,
    min_master_version="1.30.5-gke.1014003",
    location="us-east1-b",
    node_config=gcp.container.ClusterNodeConfigArgs(
        machine_type="e2-micro",
        oauth_scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
        ],
    ),
    private_cluster_config={
        "enable_private_nodes": True,
        "master_global_access_config": {
            "enabled": True,
        },
        "master_ipv4_cidr_block": "172.16.0.0/28",
    },
    deletion_protection=False,
)

# Create a second GKE cluster with IP range conflict to trigger failure mode
cluster2 = gcp.container.Cluster(
    f"{resource_name}-2",
    name=f"{resource_name}-2",
    description="GKE Cluster for testing Pulumi failure mode",
    initial_node_count=2,
    min_master_version="1.30.5-gke.1014003",
    location="us-east1-b",
    node_config=gcp.container.ClusterNodeConfigArgs(
        machine_type="e2-micro",
        oauth_scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
        ],
    ),
    private_cluster_config={
        "enable_private_nodes": True,
        "master_global_access_config": {
            "enabled": True,
        },
        "master_ipv4_cidr_block": "172.16.0.0/28",  # Intentionally create IP range conflict - Comment out to attempt repair after failure
        # "master_ipv4_cidr_block": "172.16.0.16/28",  # Fix CIDR range to repair conflict - Uncomment to attempt to repair after failure
    },
    deletion_protection=False,
    # Force dependency to ensure that first cluster is up and running for conflict to occur
    opts=pulumi.ResourceOptions(depends_on=[cluster1]),
)


# Export the cluster endpoint and kubeconfig
pulumi.export("endpoint_1", cluster1.endpoint)
pulumi.export("endpoint_2", cluster2.endpoint)
