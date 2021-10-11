import hashlib
import os


class Raid3Manager(object):
    def __init__(self, filesize, input_file) -> None:
        super().__init__()
        self.filesize = filesize
        self.input_file = input_file

    # Computes the md5 checksum for file
    def md5(self, file_name):
        hash_md5 = hashlib.md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        f.close()

        return hash_md5.hexdigest()

    def bytes_xor(self, byte1, byte2):
        return bytes([a ^ b for a, b in zip(byte1, byte2)])

    # Splice and compute the parity, directly written to the source directory.
    ## Input: Path to file.
    ## Output: Full path to the 3-part file.
    def compute_parity_hash(self):
        ctr = self.filesize

        out1_path = self.input_file + '.p1'
        out2_path = self.input_file + '.p2'
        out3_path = self.input_file + '.p3'

        with open(self.input_file, 'rb') as f:
            out1 = open(out1_path, 'wb', buffering=0)
            out2 = open(out2_path, 'wb', buffering=0)
            out3 = open(out3_path, 'wb', buffering=0)

            while ctr > 0:
                share1 = f.read(1)
                out1.write(share1)

                if ctr == 1:
                    share2 = b'0'
                else:
                    share2 = f.read(1)
                out2.write(share2)

                share3 = self.bytes_xor(share1, share2)
                out3.write(share3)

                ctr = ctr - 2

            out1.close()
            out2.close()
            out3.close()
        f.close()

        for i in range(1, 4):
            file_name = self.input_file + '.p' + str(i)
            checksum = bytearray.fromhex(self.md5(file_name))
            with open(file_name, 'ab') as fout:
                fout.write(checksum)
                fout.close()

        return (out1_path, out2_path, out3_path)

    # Joins the file
    ## Input: Path to first part of file
    def check_and_construct(self):
        ctr = self.filesize
        input_file_2 = self.input_file[:-1] + '2'

        output_file = self.input_file[:-3]

        check_1 = self.verify_checksum(self.input_file)
        check_2 = self.verify_checksum(input_file_2)

        if check_1 and check_2:
            with open(output_file, 'wb', buffering=0) as fout:
                file_part_1 = open(self.input_file, 'rb')
                file_part_2 = open(input_file_2, 'rb')
                while ctr > 0:
                    fout.write(file_part_1.read(1))

                    if ctr > 1:
                        fout.write(file_part_2.read(1))

                    ctr = ctr - 2
                fout.close()

                return 1
        else:
            input_file_3 = self.input_file[:-1] + '3'
            check_3 = self.verify_checksum(input_file_3)

            if check_3:
                if check_1:
                    with open(output_file, 'wb', buffering=0) as fout:
                        file_part_1 = open(self.input_file, 'rb')
                        file_part_3 = open(input_file_3, 'rb')

                        while ctr > 0:
                            byte_1 = file_part_1.read(1)
                            fout.write(byte_1)

                            if ctr > 1:
                                repair_byte = file_part_3.read(1)
                                fout.write(self.bytes_xor(byte_1, repair_byte))

                            ctr = ctr - 2
                        fout.close()
                elif check_2:
                    with open(output_file, 'wb', buffering=0) as fout:
                        file_part_2 = open(input_file_2, 'rb')
                        file_part_3 = open(input_file_3, 'rb')
                        while ctr > 0:
                            byte_1 = file_part_2.read(1)
                            repair_byte = file_part_3.read(1)
                            fout.write(self.bytes_xor(byte_1, repair_byte))

                            if ctr > 1:
                                fout.write(byte_1)
                            ctr = ctr - 2
                        fout.close()
                else:
                    return 0

            return 0

    def split_file_and_checksum(self, file):
        with open(file, 'rb') as f:
            filesize = os.path.getsize(file)
            input = f.read(filesize - 16)
            checksum = f.read(16)
        f.close()

        with open(file, 'wb') as fout:
            fout.write(input)
        fout.close()

        return checksum

    # Verifies the checksum of the file
    def verify_checksum(self, file):
        checksum = self.split_file_and_checksum(file)
        return bytearray.fromhex(self.md5(file)) == checksum


""" 
# test codes
filesize = compute_parity_hash(
    'C:\\Users\\nglji\\OneDrive\\Documents\\School\\CZ4010\\backend\\test\\original.txt'
)

check_and_construct(
    'C:\\Users\\nglji\\OneDrive\\Documents\\School\\CZ4010\\backend\\test\\original.txt.p1',
    filesize)
 """