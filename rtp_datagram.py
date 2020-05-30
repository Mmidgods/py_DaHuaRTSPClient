from struct import unpack


class RTPDatagram:
    '''
    RTP protocol datagram parser
    Based on github.com/plazmer/pyrtsp with minor cosmetic changes
    '''

    def __init__(self, datagram):
        self.version = 0
        self.padding = 0
        self.extension = 0
        self.csrc_count = 0
        self.marker = 0
        self.payload_type = 0
        self.sequence_number = 0
        self.timestamp = 0
        self.sync_source_id = 0
        self.csrc = []
        self.extension_header = b''
        self.extension_header_id = 0
        self.extension_header_len = 0
        self.datagram = datagram

    @property
    def datagram(self):
        return self.__datagram

    @datagram.setter
    def datagram(self, data):
        ver_p_x_cc = unpack('!B',data[:1])[0]
        m_pt = unpack('!B', data[1:2])[0]
        self.sequence_number = unpack('!H', data[2:4])[0]
        self.timestamp = unpack('!I', data[4:8])[0]
        self.sync_source_id = unpack('!I', data[8:12])[0]
        self.version = (ver_p_x_cc & 0b11000000) >> 6
        self.padding = (ver_p_x_cc & 0b00100000) >> 5
        self.extension = (ver_p_x_cc & 0b00010000) >> 4
        self.csrc_count = ver_p_x_cc & 0b00001111
        self.marker = (m_pt & 0b10000000) >> 7
        self.payload_type = m_pt & 0b01111111
        self.s_data = 0
        self.ms_data = 0

        i = 0
        for i in range(0, self.csrc_count, 4):
            self.csrc.append(unpack('!I', data[12+i:16+i]))

        if self.extension:
            i = self.csrc_count * 4
            (self.extension_header_id, self.extension_header_len) = unpack('!HH', data[12+i:16+i])
            # print(data[16+i])
            s_data = data[16+i] * 256 * 256 * 256 + data[16+i+1] * 256 * 256 + data[16+i+2] * 256 + data[16+i+3]
            ms_data = data[16+i+4] * 256 * 256 * 256 + data[16+i+5] * 256 * 256 + data[16+i+6] * 256 + data[16+i+7]
            ms_data = ms_data / pow(2, 32)
            ms_data = round(ms_data * 1000)
            self.s_data = s_data
            self.ms_data = ms_data

            # print(s_data)
            # print(ms_data)

            i += 4 + self.extension_header_len * 4

        self.payload = data[12+i:]
        self.__datagram = data

