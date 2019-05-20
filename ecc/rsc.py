
import reedsolo
import struct


class DataProcessor(object):
    def __init__(self, protocol=1):


        pass


    def pack(self, data, length=16):
        """データパック

        Arguments:
            data {bytes} -- データ

        Keyword Arguments:
            length {int} -- 符号長 (default: {16})

        Returns:
            bytes -- パック済みデータ
        """
        rs = reedsolo.RSCodec(length)

        # チェックディジット
        check_digit = self._get_check_digit(data)

        # データ長
        data_length = struct.pack("<I", len(data))

        # 符号化
        packed_data = rs.encode(data_length + data + check_digit)

        return packed_data


    def unpack(self, packed_data, length=16):
        rs = reedsolo.RSCodec(length)

        # 復号化
        decoded_data = rs.decode(packed_data)

        # データ長取得
        data_length = struct.unpack_from("<I", decoded_data, 0)[0]

        # データロード
        data = decoded_data[4:4+data_length]

        # 元データチェックディジット
        origin_check_digit = decoded_data[-1].to_bytes(1, "little")

        # チェックディジット
        check_digit = self._get_check_digit(data)

        # チェックディジット検証
        if check_digit != origin_check_digit:
            raise DataProcessorError("check digit mismatch")


        return data



    def _get_check_digit(self, data):
        check_digit = 0x00

        for digit in data:
            check_digit = check_digit ^ digit

        return check_digit.to_bytes(1, "little")


class DataProcessorError(Exception):
    def __init__(self, msg):
        super()
