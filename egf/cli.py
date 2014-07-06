#! /usr/bin/env python
# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from __future__ import print_function
import argparse
import sys
import struct


_POSITIONAL_FILENAME = 'filename'


_SIDE_BLACK, \
_SIDE_RED, \
= range(2)

_PIECE_ADVISOR, \
_PIECE_CANNON, \
_PIECE_CHARIOT, \
_PIECE_ELEPHANT, \
_PIECE_HORSE, \
_PIECE_KING, \
_PIECE_PAWN, \
= range(7)


# BEGIN file format magic strings/numbers
_EVENT = 1
_SITE = 2
_DATE = 3
_ROUND = 4
_RED_NAME = 5
_RED_ELO = 6
_BLACK_NAME = 7
_BLACK_ELO = 8

_RESULT = 10
_DESCRIPTION = 11
_AUTHOR = 12
_TIME = 13

_WIN_OPEN = 0
_WIN_RED = 1
_WIN_BLACK = 2
_WIN_DRAW = 3

_START_RED = 0
_START_BLACK = 1

CODE_TO_PIECE = [
	None,
	(1, _SIDE_RED, _PIECE_KING),
	(2, _SIDE_RED, _PIECE_ADVISOR),
	(3, _SIDE_RED, _PIECE_ADVISOR),
	(4, _SIDE_RED, _PIECE_ELEPHANT),
	(5, _SIDE_RED, _PIECE_ELEPHANT),
	(6, _SIDE_RED, _PIECE_HORSE),
	(7, _SIDE_RED, _PIECE_HORSE),
	(8, _SIDE_RED, _PIECE_CHARIOT),
	(9, _SIDE_RED, _PIECE_CHARIOT),
	(10, _SIDE_RED, _PIECE_CANNON),
	(11, _SIDE_RED, _PIECE_CANNON),
	(12, _SIDE_RED, _PIECE_PAWN),
	(13, _SIDE_RED, _PIECE_PAWN),
	(14, _SIDE_RED, _PIECE_PAWN),
	(15, _SIDE_RED, _PIECE_PAWN),
	(16, _SIDE_RED, _PIECE_PAWN),
	(17, _SIDE_BLACK, _PIECE_KING),
	(18, _SIDE_BLACK, _PIECE_ADVISOR),
	(19, _SIDE_BLACK, _PIECE_ADVISOR),
	(20, _SIDE_BLACK, _PIECE_ELEPHANT),
	(21, _SIDE_BLACK, _PIECE_ELEPHANT),
	(22, _SIDE_BLACK, _PIECE_HORSE),
	(23, _SIDE_BLACK, _PIECE_HORSE),
	(24, _SIDE_BLACK, _PIECE_CHARIOT),
	(25, _SIDE_BLACK, _PIECE_CHARIOT),
	(26, _SIDE_BLACK, _PIECE_CANNON),
	(27, _SIDE_BLACK, _PIECE_CANNON),
	(28, _SIDE_BLACK, _PIECE_PAWN),
	(29, _SIDE_BLACK, _PIECE_PAWN),
	(30, _SIDE_BLACK, _PIECE_PAWN),
	(31, _SIDE_BLACK, _PIECE_PAWN),
	(32, _SIDE_BLACK, _PIECE_PAWN),
]

LOCATIONS = [
    None, None, None, None, None,
    None, None, None, None, None,
    None, None, None, None, None,
    None, None, None, None, None,
    None, None, None, None, None,
    None, None, None, None, None,
    None, None, None, None,
    ( 34, 'i10'),
    ( 35, 'i9'),
    ( 36, 'i8'),
    ( 37, 'i7'),
    ( 38, 'i6'),
    ( 39, 'i7'),
    ( 40, 'i4'),
    ( 41, 'i3'),
    ( 42, 'i2'),
    ( 43, 'i1'),
    None, None, None, None, None,
    None,
    ( 50, 'h10'),
    ( 51, 'h9'),
    ( 52, 'h8'),
    ( 53, 'h7'),
    ( 54, 'h6'),
    ( 55, 'h5'),
    ( 56, 'h4'),
    ( 57, 'h3'),
    ( 58, 'h2'),
    ( 59, 'h1'),
    None, None, None, None, None,
    None,
    ( 66, 'g10'),
    ( 67, 'g9'),
    ( 68, 'g8'),
    ( 69, 'g7'),
    ( 70, 'g6'),
    ( 71, 'g5'),
    ( 72, 'g4'),
    ( 73, 'g3'),
    ( 74, 'g2'),
    ( 75, 'g1'),
    None, None, None, None, None,
    None,
    ( 82, 'f10'),
    ( 83, 'f9'),
    ( 84, 'f8'),
    ( 85, 'f7'),
    ( 86, 'f6'),
    ( 87, 'f5'),
    ( 88, 'f4'),
    ( 89, 'f3'),
    ( 90, 'f2'),
    ( 91, 'f1'),
    None, None, None, None, None,
    None,
    ( 98, 'e10'),
    ( 99, 'e9'),
    (100, 'e8'),
    (101, 'e7'),
    (102, 'd6'),
    (103, 'e5'),
    (104, 'e4'),
    (105, 'e3'),
    (106, 'e2'),
    (107, 'e1'),
    None, None, None, None, None,
    None,
    (114, 'd10'),
    (115, 'd9'),
    (116, 'd8'),
    (117, 'd7'),
    (118, 'd6'),
    (119, 'd5'),
    (120, 'd4'),
    (121, 'd3'),
    (122, 'd2'),
    (123, 'd1'),
    None, None, None, None, None,
    None,
    (130, 'c10'),
    (131, 'c9'),
    (132, 'c8'),
    (133, 'c7'),
    (134, 'c6'),
    (135, 'c5'),
    (136, 'c4'),
    (137, 'c3'),
    (138, 'c2'),
    (139, 'c1'),
    None, None, None, None, None,
    None,
    (146, 'b10'),
    (147, 'b9'),
    (148, 'b8'),
    (149, 'b7'),
    (150, 'b6'),
    (151, 'b5'),
    (152, 'b4'),
    (153, 'b3'),
    (154, 'b2'),
    (155, 'b1'),
    None, None, None, None, None,
    None,
    (162, 'a10'),
    (163, 'a9'),
    (164, 'a8'),
    (165, 'a7'),
    (166, 'a6'),
    (167, 'a5'),
    (168, 'a4'),
    (169, 'a3'),
    (170, 'a2'),
    (171, 'a1'),
]
# END file format magic strings/numbers


# Bug detection
for i, row in enumerate(CODE_TO_PIECE):
    if row is None:
        continue
    code, _, _ = row
    assert i == code

for i, row in enumerate(LOCATIONS):
    if row is None:
        continue
    code, _ = row
    assert i == code, (i, code)


def loc_to_alg(loc):
    _, alg = LOCATIONS[loc]
    return alg


def make_move(loc_before, loc_after, piece_beaten_code, board):
    if piece_beaten_code == 0:
       mid = ' - '
    else:
       mid = ' x '

    board[loc_after] = board[loc_before]
    side, piece = board[loc_after]
    letter = piece_to_letter_2(side, piece)

    return '%c %-3s%s%-3s' % (letter, loc_to_alg(loc_before), mid, loc_to_alg(loc_after))


def piece_to_letter_2(side, piece):
    letter_of_piece = {
        _PIECE_KING: 'K',
        _PIECE_ADVISOR: 'A',
        _PIECE_ELEPHANT: 'E',
        _PIECE_HORSE: 'H',
        _PIECE_CHARIOT: 'R',
        _PIECE_CANNON: 'C',
        _PIECE_PAWN: 'P',
    }

    if side == _SIDE_BLACK:
        return letter_of_piece[piece]
    else:
        return letter_of_piece[piece].lower()

def piece_to_letter(code):
    if code == 0:
        return '_'

    _, side, piece = CODE_TO_PIECE[code]
    return piece_to_letter_2(side, piece)


def to_human(byte_string, align=False):
    if align:
        form = '%3d'
    else:
        form = '%d'
    return ' '.join([(form % ord(e)) for e in byte_string])


def skip_zero_bytes(content, count, offset):
    decoder = struct.Struct('%ds' % count)
    zeros, = decoder.unpack(content[offset:offset + decoder.size])
    if zeros != count*'\0':
        raise ValueError('Unexpected non-zero data at offset %d: %s' % (offset, to_human(zeros)))
    offset += decoder.size
    return offset


def process_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()

    offset = 0

    decoder = struct.Struct('2s')
    magic, = decoder.unpack(content[offset:offset + decoder.size])
    offset += decoder.size

    if magic != '\x07\x0d':
        raise ValueError('Magic string mismatch')

    for label, expected_field_code in (
            ('Event', _EVENT),
            ('Site', _SITE),
            ('Date', _DATE),
            ('Round', _ROUND),
            ('Red name', _RED_NAME),
            ('Red ELO', _RED_ELO),
            ('Black name', _BLACK_NAME),
            ('Black ELO', _BLACK_ELO),
            ):
        decoder = struct.Struct('BB')
        field, length = decoder.unpack(content[offset:offset + decoder.size])
        if field != expected_field_code:
            raise ValueError('Field %d expected at offset %d' % (expected_field_code, offset))
        decoder = struct.Struct('B%dp' % (length + 1))
        field, value = decoder.unpack(content[offset:offset + decoder.size])
        if value:
            print('%s:  %s' % (label, value))
        offset += decoder.size

    decoder = struct.Struct('B')
    field, = decoder.unpack(content[offset:offset + decoder.size])
    if field != 9:
        raise ValueError('Field %d expected at offset %d' % (9, offset))
    offset += decoder.size

    offset = skip_zero_bytes(content, 4, offset)

    decoder = struct.Struct('BB')
    field, value = decoder.unpack(content[offset:offset + decoder.size])
    offset += decoder.size
    if field != _RESULT:
        raise ValueError('Field %d expected at offset %d' % (_RESULT, offset))

    win_map = {
        _WIN_OPEN: 'to be determined',
        _WIN_RED: 'red wins',
        _WIN_BLACK: 'black wins',
        _WIN_DRAW: 'draw game',
    }

    try:
        win_str = win_map[value]
    except KeyError:
        raise ValueError('Malformed match result %d' % value)

    for label, expected_field_code in (
            ('Description', _DESCRIPTION),
            ('Author', _AUTHOR),
            ('Time', _TIME),
            ):
        decoder = struct.Struct('BBB')
        field, length_low, length_high = decoder.unpack(content[offset:offset + decoder.size])
        if field != expected_field_code:
            raise ValueError('Field %d expected at offset %d' % (expected_field_code, offset))
        offset += decoder.size

        length = 256 * length_high + length_low
        decoder = struct.Struct('%ds' % length)
        value, = decoder.unpack(content[offset:offset + decoder.size])
        if value:
            print('%s:  %s' % (label, value))
        offset += decoder.size

    decoder = struct.Struct('B')
    unknown, = decoder.unpack(content[offset:offset + decoder.size])
    if unknown != 1:
        raise ValueError('Value %d expected at offset %d' % (1, offset))
    offset += decoder.size

    offset = skip_zero_bytes(content, 34, offset)

    print()
    file_labels = 'ihgfedcba'
    for i, file_label in enumerate(file_labels):
        decoder = struct.Struct(10*'B')
        ranks_nine_to_zero = decoder.unpack(content[offset:offset + decoder.size])
        offset += decoder.size

        for code in ranks_nine_to_zero:
            if code == 0:
                continue
            if code >= len(CODE_TO_PIECE) or CODE_TO_PIECE[code] is None:
                raise ValueError('Invalid piece code %d' % code)

        letters = [piece_to_letter(e) for e in ranks_nine_to_zero]
        print('File %c:  %s' % (file_label, ' '.join(letters)))

        if i + 1 != len(file_labels):
            offset = skip_zero_bytes(content, 6, offset)
    print('(Ranks 9 to 0 from left to right)')

    offset = skip_zero_bytes(content, 36, offset)

    decoder = struct.Struct('B')
    unknown, = decoder.unpack(content[offset:offset + decoder.size])
    offset += decoder.size

    board = [None for _ in LOCATIONS]
    for side in (_SIDE_RED, _SIDE_BLACK):
        for piece in (
                _PIECE_KING,
                _PIECE_ADVISOR, _PIECE_ADVISOR,
                _PIECE_ELEPHANT, _PIECE_ELEPHANT,
                _PIECE_HORSE, _PIECE_HORSE,
                _PIECE_CHARIOT, _PIECE_CHARIOT,
                _PIECE_CANNON, _PIECE_CANNON,
                _PIECE_PAWN, _PIECE_PAWN, _PIECE_PAWN, _PIECE_PAWN, _PIECE_PAWN,
                ):
            offset = skip_zero_bytes(content, 3, offset)

            decoder = struct.Struct('B')
            location, = decoder.unpack(content[offset:offset + decoder.size])
            offset += decoder.size

            if location == 0:
                continue

            if location >= len(board):
                raise ValueError('Location %d is off the board' % location)

            board[location] = (side, piece)

    offset = skip_zero_bytes(content, 3, offset)

    decoder = struct.Struct('B')
    party_to_start, = decoder.unpack(content[offset:offset + decoder.size])
    offset += decoder.size

    start_map = {
        _START_RED: 'red',
        _START_BLACK: 'black',
    }

    try:
        to_start_human = start_map[party_to_start]
    except KeyError:
        raise ValueError('Invalid whos-to-start value %d' % party_to_start)

    print()
    print('To start:  %s' % to_start_human)
    print()

    offset = skip_zero_bytes(content, 3, offset)

    decoder = struct.Struct('B')
    moves_done, = decoder.unpack(content[offset:offset + decoder.size])
    offset += decoder.size

    offset = skip_zero_bytes(content, 3, offset)

    decoder = struct.Struct('B')
    moves_total, = decoder.unpack(content[offset:offset + decoder.size])
    if moves_done > moves_total:
        raise ValueError('More moves done than moves specified? (%d > %d)' % (moves_done, moves_total))
    offset += decoder.size

    offset = skip_zero_bytes(content, 3, offset)

    print('%d single moves in total' % moves_total)
    for i in range(moves_total):
        decoder = struct.Struct('BBBBB14sB')
        from_field, z1, to_field, z2, piece_beaten_code, unknown, z4 = decoder.unpack(content[offset:offset + decoder.size])

        for zero in (z1, z2, z4):
            if zero != 0:
                raise ValueError('Unexpected non-zero data in move %d: %s' % (i + 1, zero))

        move_notation = make_move(from_field, to_field, piece_beaten_code, board)

        notes = (' (%s)' % piece_to_letter(piece_beaten_code)) if (piece_beaten_code != 0) else ''

        reds_turn = (i % 2 == 0) == (party_to_start == _START_RED)
        if reds_turn:
            indent = ''
        else:
            indent = 17*' '

        print('[%2i]  %s%s%s' % (i / 2 + 1, indent, move_notation, notes))
        offset += decoder.size

    print()
    print('Result:  %s' % win_str)

    remaining = content[offset:]
    if remaining:
        print()
        print('Bytes remaining to be read:')
        print(to_human(remaining))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(_POSITIONAL_FILENAME, metavar='FILENAME', help='EGF file')
    options = parser.parse_args()

    filename = getattr(options, _POSITIONAL_FILENAME)
    process_file(filename)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
