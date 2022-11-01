import mysql.connector
import pandas as pd

# from google.cloud.sql.connector import Connector, IPTypes


mydb = mysql.connector.connect(
    host="34.118.109.6",
    user="root",
    password="123456",
    database="score_table"
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE tennis_scores")

# my_cursor.execute("SHOW DATABASES")

# my_cursor.execute("CREATE TABLE scores (id INT AUTO_INCREMENT PRIMARY KEY, player VARCHAR(255), score INT)")

# my_cursor.execute("SELECT * FROM scores")

my_cursor.execute("DROP TABLE scores")

my_cursor.execute("CREATE TABLE scores (id INT AUTO_INCREMENT PRIMARY KEY, player VARCHAR(255), score INT)")


# my_cursor.execute("SHOW TABLES")
# for x in my_cursor:
#     print(x)

df = pd.read_csv('scores.csv')

for i in range(len(df)):
    player_name = df.Player[i]
    player_score = df.Score[i]
    sql_command = "INSERT INTO scores (player, score) VALUES('" + player_name + "'," +  str(player_score) + ")"
    my_cursor.execute(sql_command)

my_cursor.execute("COMMIT")


# my_cursor.execute("INSERT INTO scores (player, score) VALUES('can', 800)")
# my_cursor.execute("INSERT INTO scores (player, score) VALUES('uraz', 800)")

my_cursor.execute("SELECT * FROM scores WHERE player = 'Can'")
# my_cursor.execute("SELECT * FROM scores WHERE player = 'Burak'")



for x in my_cursor:
    print(x)

my_cursor.execute("SELECT * FROM scores WHERE player like 'B%'")
for x in my_cursor:
    print(x)


# export GOOGLE_CLOUD_PROJECT=scores-364816

# mkdir some_dir && cd some_dir && nano main.tf

import os

import sqlalchemy


# connect_unix_socket initializes a Unix socket connection pool for
# a Cloud SQL instance of MySQL.
def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_user = os.environ["root"]  # e.g. 'my-database-user'
    db_pass = os.environ["123456"]  # e.g. 'my-database-password'
    db_name = os.environ["score_table"]  # e.g. 'my-database'
    unix_socket_path = os.environ["/cloudsql/scores-364816:europe-central2:adi-tennis-db"]  # e.g. '/cloudsql/project:region:instance'

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": unix_socket_path},
        ),
        # ...
    )
    return pool



#     gcloud sql instances describe adi-tennis-db

#     backendType: SECOND_GEN


# backendType: SECOND_GEN
# connectionName: scores-364816:europe-central2:adi-tennis-db
# createTime: '2022-10-21T21:35:56.249Z'
# databaseInstalledVersion: MYSQL_8_0_26
# databaseVersion: MYSQL_8_0
# etag: b7ca5b0a448f1fe97bf616ef5091f97ebd3398d08345a98b7812b6acd747f617
# failoverReplica:
#   available: true
# gceZone: europe-central2-a
# instanceType: CLOUD_SQL_INSTANCE
# ipAddresses:
# - ipAddress: 34.118.20.170
#   type: PRIMARY
# kind: sql#instance
# maintenanceVersion: MYSQL_8_0_26.R20220809.02_02
# name: adi-tennis-db
# project: scores-364816
# region: europe-central2
# secondaryGceZone: europe-central2-b
# selfLink: https://sqladmin.googleapis.com/sql/v1beta4/projects/scores-364816/instances/adi-tennis-db
# serverCaCert:
#   cert: |-
#     -----BEGIN CERTIFICATE-----
#     MIIDfzCCAmegAwIBAgIBADANBgkqhkiG9w0BAQsFADB3MS0wKwYDVQQuEyRjYmVh
#     OWJiZi1iZDIwLTQwOWYtYjRmZS01NzA4NTUyOTM0NGMxIzAhBgNVBAMTGkdvb2ds
#     ZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUsIEluYzELMAkG
#     A1UEBhMCVVMwHhcNMjIxMDIxMjEzOTM2WhcNMzIxMDE4MjE0MDM2WjB3MS0wKwYD
#     VQQuEyRjYmVhOWJiZi1iZDIwLTQwOWYtYjRmZS01NzA4NTUyOTM0NGMxIzAhBgNV
#     BAMTGkdvb2dsZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUs
#     IEluYzELMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
#     AQCjUvowrQQv4U/NbeXNbfVYpPbE7Pe+FyZaZQ8kVVZbS7WrIL6s+OyNVydUOuII
#     37PfdH5y3MV2GrfH2O1yUhoKakUlXMY/xGh+1ePvQd94aWKMM/dx/BCylT+6kH2D
#     k2Nbo2hrTtxWw9tOVthrprTTptlDe3FS744QdPGwubiF7PbFsS4YpRY2si7YCTgN
#     HTrv5vLQEopbOHlDgqZRthpJfoZip/jfm1zyzNI2NrmonGyD0OtA7J9pXP6d0AZz
#     XEzejvy+cBZ3jb2EKoqiUzq2IxnaYMX65eSHJwYNs8hTO3AlXuy85xkD2gvibt5E
#     s3adj4XQ+l5ONF+wu6YrKCDRAgMBAAGjFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAw
#     DQYJKoZIhvcNAQELBQADggEBADd7E0f67cLrX5RW1o15VWIl5OT3yWxPXK8m1XHf
#     i7LWuO2HR9q2eXQfgqDYcbiIS4MtrrQaWWKK1rv6noEOMhftLHGFmSKp/76dy7op
#     92yVmvnK1BhIa9vGSGNp3dAfi/kLjDUCohWh3TYQB00gqzgWtBap/MdRdLE0SWxN
#     /8kDmZ0X4YUiGlKQS+hASrAlxyGKHdGJVfWloe93S4H9A/lZGikxn4wK0utsMbpV
#     VIlMu8vmLlUL43w5fqoT4H6ZExLCwmZqz0eIwNdx9fNcPla3aEp/x46lJa0ZUO0O
#     FUQ/hU/zKOX/huCb9qI4KTrwQYNFl85GLp+s4gnDvBgssro=
#     -----END CERTIFICATE-----
#   certSerialNumber: '0'
#   commonName: C=US,O=Google\, Inc,CN=Google Cloud SQL Server CA,dnQualifier=cbea9bbf-bd20-409f-b4fe-57085529344c
#   createTime: '2022-10-21T21:39:36.657Z'
#   expirationTime: '2032-10-18T21:40:36.657Z'
#   instance: adi-tennis-db
#   kind: sql#sslCert
#   sha1Fingerprint: 2bd6acccaf67bfd800e55e4519fd77905add4387
# serviceAccountEmailAddress: p549690191909-nvs05x@gcp-sa-cloud-sql.iam.gserviceaccount.com
# settings:
#   activationPolicy: ALWAYS
#   availabilityType: REGIONAL
#   backupConfiguration:
#     backupRetentionSettings:
#       retainedBackups: 7
#       retentionUnit: COUNT
#     binaryLogEnabled: true
#     enabled: true
#     kind: sql#backupConfiguration
#     location: eu
#     startTime: 14:00
#     transactionLogRetentionDays: 7
#   connectorEnforcement: NOT_REQUIRED
#   dataDiskSizeGb: '100'
#   dataDiskType: PD_SSD
#   deletionProtectionEnabled: true
#   ipConfiguration:
#     authorizedNetworks:
#     - kind: sql#aclEntry
#       name: ''
#       value: 24.133.128.152
#     ipv4Enabled: true
#   kind: sql#settings
#   locationPreference:
#     kind: sql#locationPreference
#     zone: europe-central2-a
#   maintenanceWindow:
#     day: 0
#     hour: 0
#     kind: sql#maintenanceWindow
#     updateTrack: stable
#   pricingPlan: PER_USE
#   replicationType: SYNCHRONOUS
#   settingsVersion: '21'
#   storageAutoResize: true
#   storageAutoResizeLimit: '0'
#   tier: db-custom-4-26624
# state: RUNNABLE