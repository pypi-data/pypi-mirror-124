from gkutils.commonutils import readGenericDataFile
from cassandra.cluster import Cluster
from ingestGenericDatabaseTable import executeLoad

# OK - so it looks like if you want to test stuff, they all have to be inside the test_ function.

def test_me():
    class EmptyClass:
        pass

    # Setup the test - read the test data from the input file. Connect to the database.
    def setup(options):
        inputData = readGenericDataFile(options.filename, delimiter = options.delimiter)
        return inputData

    # Exercise the code - insert the test data
    def run(options, inputData):
        db = {'hostname': options.hostname, 'keyspace': options.keyspace}
        cluster = Cluster(db['hostname'])
        session = cluster.connect()
        session.set_keyspace(db['keyspace']) 

        executeLoad(session, options.table, inputData, types = options.types)

        cluster.shutdown()

    # Verify the test - read the test data from the database
    def verify(options, inputData):
        db = {'hostname': options.hostname, 'keyspace': options.keyspace}
        cluster = Cluster(db['hostname'])
        session = cluster.connect()
        session.set_keyspace(db['keyspace']) 

        # Yeah, I need to setup the verification. Let's get the thing executing first.
        # Executes from the command line, but will not execute in pytest.

        cluster.shutdown()


    # Cleanup - truncate the test table. Disconnect from the database.
    def cleanup(options):
        db = {'hostname': options.hostname, 'keyspace': options.keyspace}
        cluster = Cluster(db['hostname'])
        session = cluster.connect()
        session.set_keyspace(db['keyspace']) 

#        session.execute("truncate table test_noncandidates;")

        cluster.shutdown()



    options = EmptyClass()
    options.hostname = ['localhost']
    options.keyspace = 'test01'
    options.filename = '/Users/kws/lasair/cassandra/load-old-data/noncandidates/test_100_rows.csv'
    options.table = 'test_noncandidates'
    options.delimiter = ','
    # The test is reading a CSV file with no schema types. So add the types.
    options.types = "str,float,float,int,int,float,float,float,int".split(',')

    testData = setup(options)
    run(options, testData)
    verify(options, testData)
    cleanup(options)

if __name__ == '__main__':
    test_me()

