#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Commandline scripts.

These scripts are called by the executables defined in setup.py.
"""

import abc
import sys
import typing
import optparse

from . import newkeys, PublicKey, encrypt, PrivateKey, decrypt, verify, sign, VerificationError
from .key import AbstractKey
from .pkcs1 import HASH_METHODS

HASH_METHODS = sorted(HASH_METHODS.keys())
Indexable = typing.Union[typing.Tuple, typing.List[str]]


def keygen() -> None:
    """Key generator."""

    # Parse the CLI options
    parser = optparse.OptionParser(usage='usage: %prog [options] keysize',
                                   description='Generates a new RSA keypair of "keysize" bits.')

    parser.add_option('--pubout', type='string',
                      help='Output filename for the public key. The public key is '
                           'not saved if this option is not present. You can use '
                           'pyrsa-priv2pub to create the public key file later.')

    parser.add_option('-o', '--out', type='string',
                      help='Output filename for the private key. The key is '
                           'written to stdout if this option is not present.')

    parser.add_option('--form',
                      help='key format of the private and public keys - default PEM',
                      choices=('PEM', 'DER'), default='PEM')

    (cli, cli_args) = parser.parse_args(sys.argv[1:])

    if len(cli_args) != 1:
        parser.print_help()
        raise SystemExit(1)

    try:
        keysize = int(cli_args[0])
    except ValueError:
        parser.print_help()
        print('Not a valid number: %s' % cli_args[0], file=sys.stderr)
        raise SystemExit(1)

    print('Generating %i-bit key' % keysize, file=sys.stderr)
    (pub_key, priv_key) = newkeys(keysize)

    # Save public key
    if cli.pubout:
        print('Writing public key to %s' % cli.pubout, file=sys.stderr)
        data = pub_key.save_pkcs1(format=cli.form)
        with open(cli.pubout, 'wb') as outfile:
            outfile.write(data)

    # Save private key
    data = priv_key.save_pkcs1(format=cli.form)

    if cli.out:
        print('Writing private key to %s' % cli.out, file=sys.stderr)
        with open(cli.out, 'wb') as outfile:
            outfile.write(data)
    else:
        print('Writing private key to stdout', file=sys.stderr)
        sys.stdout.buffer.write(data)


class CryptoOperation(metaclass=abc.ABCMeta):
    """CLI callable that operates with input, output, and a key."""

    keyname = 'public'  # or 'private'
    usage = 'usage: %%prog [options] %(keyname)s_key'
    description = ''
    operation = 'decrypt'
    operation_past = 'decrypted'
    operation_progressive = 'decrypting'
    input_help = 'Name of the file to %(operation)s. Reads from stdin if ' \
                 'not specified.'
    output_help = 'Name of the file to write the %(operation_past)s file ' \
                  'to. Written to stdout if this option is not present.'
    expected_cli_args = 1
    has_output = True

    key_class = PublicKey  # type: typing.Type[AbstractKey]

    def __init__(self) -> None:
        self.usage = self.usage % self.__class__.__dict__
        self.input_help = self.input_help % self.__class__.__dict__
        self.output_help = self.output_help % self.__class__.__dict__

    @abc.abstractmethod
    def perform_operation(self, indata: bytes, key: AbstractKey,
                          cli_args: Indexable) -> typing.Any:
        """Performs the program's operation.

        Implement in a subclass.

        :returns: the data to write to the output.
        """

    def __call__(self) -> None:
        """Runs the program."""

        (cli, cli_args) = self.parse_cli()

        key = self.read_key(cli_args[0], cli.keyform)

        indata = self.read_infile(cli.input)

        print(self.operation_progressive.title(), file=sys.stderr)
        outdata = self.perform_operation(indata, key, cli_args)

        if self.has_output:
            self.write_outfile(outdata, cli.output)

    def parse_cli(self) -> typing.Tuple[optparse.Values, typing.List[str]]:
        """Parse the CLI options

        :returns: (cli_opts, cli_args)
        """

        parser = optparse.OptionParser(usage=self.usage, description=self.description)

        parser.add_option('-i', '--input', type='string', help=self.input_help)

        if self.has_output:
            parser.add_option('-o', '--output', type='string', help=self.output_help)

        parser.add_option('--keyform',
                          help='Key format of the %s key - default PEM' % self.keyname,
                          choices=('PEM', 'DER'), default='PEM')

        (cli, cli_args) = parser.parse_args(sys.argv[1:])

        if len(cli_args) != self.expected_cli_args:
            parser.print_help()
            raise SystemExit(1)

        return cli, cli_args

    def read_key(self, filename: str, keyform: str) -> AbstractKey:
        """Reads a public or private key."""

        print('Reading %s key from %s' % (self.keyname, filename), file=sys.stderr)
        with open(filename, 'rb') as keyfile:
            keydata = keyfile.read()

        return self.key_class.load_pkcs1(keydata, keyform)

    def read_infile(self, inname: str) -> bytes:
        """Read the input file"""

        if inname:
            print('Reading input from %s' % inname, file=sys.stderr)
            with open(inname, 'rb') as infile:
                return infile.read()

        print('Reading input from stdin', file=sys.stderr)
        return sys.stdin.buffer.read()

    def write_outfile(self, outdata: bytes, outname: str) -> None:
        """Write the output file"""

        if outname:
            print('Writing output to %s' % outname, file=sys.stderr)
            with open(outname, 'wb') as outfile:
                outfile.write(outdata)
        else:
            print('Writing output to stdout', file=sys.stderr)
            sys.stdout.buffer.write(outdata)


class EncryptOperation(CryptoOperation):
    """Encrypts a file."""

    keyname = 'public'
    description = ('Encrypts a file. The file must be shorter than the key '
                   'length in order to be encrypted.')
    operation = 'encrypt'
    operation_past = 'encrypted'
    operation_progressive = 'encrypting'

    def perform_operation(self, indata: bytes, pub_key: AbstractKey,
                          cli_args: Indexable = ()) -> bytes:
        """Encrypts files."""
        assert isinstance(pub_key, PublicKey)
        return encrypt(indata, pub_key)


class DecryptOperation(CryptoOperation):
    """Decrypts a file."""

    keyname = 'private'
    description = ('Decrypts a file. The original file must be shorter than '
                   'the key length in order to have been encrypted.')
    operation = 'decrypt'
    operation_past = 'decrypted'
    operation_progressive = 'decrypting'
    key_class = PrivateKey

    def perform_operation(self, indata: bytes, priv_key: AbstractKey,
                          cli_args: Indexable = ()) -> bytes:
        """Decrypts files."""
        assert isinstance(priv_key, PrivateKey)
        return decrypt(indata, priv_key)


class SignOperation(CryptoOperation):
    """Signs a file."""

    keyname = 'private'
    usage = 'usage: %%prog [options] private_key hash_method'
    description = ('Signs a file, outputs the signature. Choose the hash '
                   'method from %s' % ', '.join(HASH_METHODS))
    operation = 'sign'
    operation_past = 'signature'
    operation_progressive = 'Signing'
    key_class = PrivateKey
    expected_cli_args = 2

    output_help = ('Name of the file to write the signature to. Written '
                   'to stdout if this option is not present.')

    def perform_operation(self, indata: bytes, priv_key: AbstractKey,
                          cli_args: Indexable) -> bytes:
        """Signs files."""
        assert isinstance(priv_key, PrivateKey)

        hash_method = cli_args[1]
        if hash_method not in HASH_METHODS:
            raise SystemExit('Invalid hash method, choose one of %s' %
                             ', '.join(HASH_METHODS))

        return sign(indata, priv_key, hash_method)


class VerifyOperation(CryptoOperation):
    """Verify a signature."""

    keyname = 'public'
    usage = 'usage: %%prog [options] public_key signature_file'
    description = ('Verifies a signature, exits with status 0 upon success, '
                   'prints an error message and exits with status 1 upon error.')
    operation = 'verify'
    operation_past = 'verified'
    operation_progressive = 'Verifying'
    key_class = PublicKey
    expected_cli_args = 2
    has_output = False

    def perform_operation(self, indata: bytes, pub_key: AbstractKey,
                          cli_args: Indexable) -> None:
        """Verifies files."""
        assert isinstance(pub_key, PublicKey)

        signature_file = cli_args[1]

        with open(signature_file, 'rb') as sigfile:
            signature = sigfile.read()

        try:
            verify(indata, signature, pub_key)
        except VerificationError:
            raise SystemExit('Verification failed.')

        print('Verification OK', file=sys.stderr)


encrypt = EncryptOperation()
decrypt = DecryptOperation()
sign = SignOperation()
verify = VerifyOperation()
