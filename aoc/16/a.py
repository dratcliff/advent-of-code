from utilaoc import file_to_strings

actual = file_to_strings("a.txt")


class Packet:
    def __init__(self, version, type):
        self.version = version
        self.type = type
        self.literal = ""
        self.sub_packets = []

    def value(self):
        if self.type == 0:
            return sum([x.value() for x in self.sub_packets])
        elif self.type == 1:
            s = 1
            for packet in self.sub_packets:
                s *= packet.value()
            return s
        elif self.type == 2:
            return min(self.sub_packets, key=lambda x: x.value()).value()
        elif self.type == 3:
            return max(self.sub_packets, key=lambda x: x.value()).value()
        elif self.type == 5:
            if self.sub_packets[0].value() > self.sub_packets[1].value():
                return 1
            return 0
        elif self.type == 6:
            if self.sub_packets[0].value() < self.sub_packets[1].value():
                return 1
            return 0
        elif self.type == 7:
            if self.sub_packets[0].value() == self.sub_packets[1].value():
                return 1
            return 0
        return self.literal


conversion = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def to_binary_string(hex):
    s = ""
    for v in hex:
        s += conversion[v]
    return s


def to_packets(s, packets, todo_p, todo_b, pos):
    cur = pos
    more = True
    while more:
        more = False
        version = int(s[cur:cur+3], 2)
        cur += 3
        todo_b -= 3
        type = int(s[cur:cur+3], 2)
        cur += 3
        todo_b -= 3
        packet = Packet(version, type)
        if packet.type == 4:
            prefix = int(s[cur], 2)
            literal = ""
            while prefix == 1:
                cur += 1
                todo_b -= 1
                literal += s[cur:cur+4]
                cur += 4
                todo_b -= 4
                prefix = int(s[cur], 2)
            cur += 1
            todo_b -= 1
            literal += s[cur:cur+4]
            cur += 4
            todo_b -= 4
            todo_p -= 1
            packet.literal = int(literal, 2)
            packets.append(packet)
            if todo_b > 0 or todo_p > 0:
                more = True
            else:
                return (packets, cur)
        else:
            length_type = int(s[cur], 2)
            cur += 1
            if length_type == 0:
                todo_b -= 1
                todo_b = int(s[cur:cur+15], 2)
                cur += 15
                while todo_b > 0:
                    subpackets, new_cur = to_packets(s, [], -1, todo_b, cur)
                    packet.sub_packets += subpackets
                    todo_b -= (new_cur-cur)
                    cur = new_cur
            else:
                todo_p = int(s[cur:cur+11], 2)
                cur += 11
                while todo_p > 0:
                    subpackets, cur = to_packets(s, [], todo_p, -1, cur)
                    packet.sub_packets += subpackets
                    todo_p -= len(subpackets)
            packets.append(packet)
            return (packets, cur)
    return (packets, cur)


binary_packet = to_binary_string(actual[0])
packets, pos = to_packets(binary_packet, [], -1, -1, 0)

version_sum = 0


def sumv(packets):
    global version_sum
    for packet in packets:
        version_sum += packet.version
        sumv(packet.sub_packets)


sumv(packets)
print(version_sum)

print(packets[0].value())
