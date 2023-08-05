from pyspark.sql import SparkSession
from pyspark.sql import HiveContext


def spark_initializer(app_name, args):

    input_datastorage_type = ""
    output_datastorage_type = ""

    if "dataStorageType-input-dataset" in args:
        input_datastorage_type = args["dataStorageType-input-dataset"].lower()

    if "dataStorageType-output-dataset" in args:
        output_datastorage_type = args["dataStorageType-output-dataset"].lower()

    if input_datastorage_type.startswith("hive"):
        spark = SparkSession \
            .builder \
            .appName(app_name) \
            .config('spark.sql.warehouse.dir', '/warehouse/tablespace/managed/hive') \
            .config("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true") \
            .config('hive.metastore.uris', args["hiveMetastoreUris-input-dataset"]) \
            .config('spark.hadoop.dfs.client.use.datanode.hostname', True) \
            .config('javax.jdo.option.ConnectionUserName', args["hiveUserName-input-dataset"]) \
            .config('javax.jdo.option.ConnectionPassword', args["hivePassword-input-dataset"]) \
            .config('hive.server2.enable.doAs', True) \
            .config('hive.metastore.client.connect.retry.delay', 5) \
            .config('hive.metastore.client.socket.timeout', 1800) \
            .enableHiveSupport() \
            .getOrCreate()
    elif output_datastorage_type.startswith("hive"):
        spark = SparkSession \
            .builder \
            .appName(app_name) \
            .config('spark.sql.warehouse.dir', '/warehouse/tablespace/managed/hive') \
            .config("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true") \
            .config('hive.metastore.uris', args["hiveMetastoreUris-output-dataset"]) \
            .config('spark.hadoop.dfs.client.use.datanode.hostname', True) \
            .config('javax.jdo.option.ConnectionUserName', args["hiveUserName-output-dataset"]) \
            .config('javax.jdo.option.ConnectionPassword', args["hivePassword-output-dataset"]) \
            .config('hive.server2.enable.doAs', True) \
            .config('hive.metastore.client.connect.retry.delay', 5) \
            .config('hive.metastore.client.socket.timeout', 1800) \
            .enableHiveSupport() \
            .getOrCreate()

        # Hive session
        hive = HiveContext(spark)
    else:
        spark = SparkSession.builder.appName(app_name).getOrCreate()

    return spark
