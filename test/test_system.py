import unittest
import subprocess
import shlex


class TestSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seeds = 'seed.openbazaar.org seed2.openbazaar.org seed.openlabs.co us.seed.bizarre.company eu.seed.bizarre.company'
        cls.db_file = 'db/test.db'
        cls.port = '12345'
        cls.http_ip = '127.0.0.1'
        cls.http_port = '-1'
        cls.http_opts = '-k %s -q %s' % (cls.http_ip, cls.http_port)
        cls.bm_user = 'tester'
        cls.bm_pass = 'secret'
        cls.bm_port = '8442'
        cls.bm_opts = '--bmuser %s --bmpass %s --bmport %s' % (cls.bm_user, cls.bm_pass, cls.bm_port)
        cls.net_opts = '%s -p %s --disable_upnp' % (cls.http_opts, cls.port)
        cls.db_opts = '--database %s' % (cls.db_file)
        cls.crypto_opts = '--disable_sqlite_crypt'
        cls.seed_opts = '-S %s' % (cls.seeds)
        cls.log_dir = 'logs'
        cls.log_file = '%s/test.log' % (cls.log_dir)
        cls.log_level = '10' # debug
        cls.log_opts = '-l %s --log_level %s' % (cls.log_file, cls.log_level)
        cls.misc_opts = '-u 1 --disable_open_browser --disable-ip-update 127.0.0.1'
        cls.cmd = "python node/openbazaar_daemon.py %s" % (
            ' '.join((
                cls.net_opts, cls.bm_opts,
                cls.db_opts, cls.seed_opts,
                cls.log_opts, cls.misc_opts,
                cls.crypto_opts
            ))
        )

    def run_system(self):
        p = subprocess.Popen(shlex.split(self.cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_data = p.stdout.read()
        stderr_data = p.stderr.read()

        return (stdout_data, stderr_data)

    def assertSystemError(self, expected_error):
        _, err = self.run_system()
        return expected_error in err

    def test_empty_db(self):
        self.assertSystemError('database file %s corrupt' % (self.db_file))

#    def test_create_db(self):
#        cmd = "python node/setup_db.py %s %s" % (self.db_file, self.crypto_opts)
#
#        self.assertEquals(0, subprocess.call(shlex.split(cmd)))
