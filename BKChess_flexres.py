#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# WORK IN PROGRESS
# for questions or advice mail me at:
# bart.berkel at gmail.com

import random
import pygame
# screen init
pygame.init()
dispsize = input('The display size will be SxS. Give S:\n')
relsize = dispsize / 8
screen = pygame.display.set_mode((dispsize, dispsize))
screen.fill((160, 160, 160))
f = open('ChessAlpha2.ttf')
myfont = pygame.font.Font(f, relsize)

pygame.display.flip()

# globals
borddict = {}
situationsdict1 = {}
situationsdict2 = {}
Box = {0: [], 1: [], -1: []}
fiftycount = 1
count = 1
check = False
enpassantdict = {}
hascastled = False
kingslist = ['dummy']
rookslist = ['dummy']
R9 = range(1, 9)


class Piece(object):

    def __init__(self, type_, cstr, color, worth, coord, img=0):
        self.L = coord[0]
        self.N = coord[1]
        self.img = myfont.render(img, True, (0, 0, 0)) if img  else img
        self.name = type_ + cstr
        self.img = pygame.transform.chop(self.img, pygame.Rect(0, (relsize*0.8), (relsize*0.6), relsize)) if self.name == 'RookBlack' else self.img
        self.pos = self.img.get_rect() if img  else 0
        self.cstr = cstr
        self.type = type_
        self.color = color
        self.worth = worth
        self.attacked = False
        self.unmoved = True
        self.coord = coord
        borddict[(self.L, self.N)] = self
    
    def moveimg(self):
            L, N = self.coord
            L -= 1
            N -= 1
            shade = (255, 255, 255) if (L-N) % 2 == 0 else (255, 220, 140)
            squarerect = pygame.Rect(L*relsize, N*relsize, relsize, relsize)
            screen.fill(shade, squarerect)
            if self.img:
                self.pos = self.img.get_rect()
                self.pos = self.pos.move((L*relsize)+(relsize/5), N*relsize)
                screen.blit(self.img, self.pos)
            pygame.display.flip()


# function that generates possible new positions
def step_iter(L, N, stepL, stepN):
    while 1:
            L += stepL
            N += stepN
            yield L, N

# function that determines viable steps using the position generator
def viable_steps(piece):
    global enpassantdict
    L, N = piece.coord
    type_ = piece.type
    color = piece.color
    Reach = R9
    viablepositionlist = []
    steplist = []
    Diasteps = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    Strsteps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    Hrssteps = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1),
                        (-1, -2), (1, -2), (2, -1)]
    if type_ == 'Pawn':
        diastep1, diastep2 = (L-1, N-color), (L+1, N-color)
        strstep = (L, N-color)
        for pstep in [diastep1, diastep2]:
            if pstep[0] in R9 and pstep[1] in R9:
                if borddict[pstep].color == -color or \
                        pstep in enpassantdict:
                    viablepositionlist.append(pstep)
            else:
                continue
        if strstep[0] in R9 and strstep[1] in R9:
            if not borddict[strstep].color:
                viablepositionlist.append(strstep)
                strstep = (strstep[0], strstep[1]-color)
                if piece.unmoved and not borddict[strstep].color:
                    viablepositionlist.append(strstep)
        return viablepositionlist
    elif type_ == 'Bishop':
        steplist.extend(Diasteps)
    elif type_ == 'Rook':
        steplist.extend(Strsteps)
    elif type_ == 'Hnight':
        steplist = Hrssteps
        Reach = [1]
    else:
        steplist.extend(Strsteps)
        steplist.extend(Diasteps)
        if piece.type == 'King':
            Reach = [1]
    for direction in steplist:
        stepL, stepN = direction
        newline = step_iter(L, N, stepL, stepN)
        for i in Reach:
            new_step = next(newline)
            if not new_step[0] in R9 or not new_step[1] in R9:
                break
            elif borddict[new_step].color == color:
                break
            elif borddict[new_step].color == -color:
                viablepositionlist.append(new_step)
                break
            else:
                viablepositionlist.append(new_step)
    return viablepositionlist

# Instatiating all pieces, including empty fields.
# Kings are listed, using dummy to make for colorbased (-1 or 1) indexing
# So are the rooks.
fontpieceslist = [['dummy'], ['i', 'k', 'j', 'l', 'm', 'n'], ['I', 'K', 'J',' L', 'M', 'N']]
for L in R9:
    for N in R9:
        Piece('_ield', 'Neutr', 0, 0, (L, N))
for player in [[1, 'White', [8, 7]], [-1, 'Black',  [1, 2]]]:
    rooks = []
    R = player[2][0]
    Rp = player[2][1]
    C = player[0]
    c = player[1]
    fontpiecescol = fontpieceslist[C]
    newpiece = Piece('Rook', c, C, 5, (8, R), img=fontpiecescol[3])
    rooks.append(newpiece)
    newpiece = Piece('Rook', c, C, 5, (1, R), img=fontpiecescol[3])
    rooks.append(newpiece)
    newpiece = Piece('Hnight', c, C, 3, (2, R), img=fontpiecescol[1])
    newpiece = Piece('Hnight', c, C, 3, (7, R), img=fontpiecescol[1])
    newpiece = Piece('Bishop', c, C, 3, (3, R), img=fontpiecescol[2])
    newpiece = Piece('Bishop', c, C, 3, (6, R), img=fontpiecescol[2])
    newpiece = Piece('King', c, C, 0, (5, R), img=fontpiecescol[5])
    kingslist.append(newpiece)
    newpiece = Piece('Queen', c, C, 9, (4, R), img=fontpiecescol[4])
    rookslist.append(rooks)
    for L in R9:
        newpiece = Piece('Pawn', c, C, 1, (L, Rp), img=fontpiecescol[0])
for item in borddict.items():
    square, piece = item
    piece.moveimg()

# function that handles pawn promotion
def picknewpiece(piece, nwsq):
    global Box
    C = piece.color
    c = piece.cstr
    fontpiecescol = fontpieceslist[C]
    newpiece = random.choice([1, 2, 2])
    Box[piece.color].append(piece)
    if newpiece == 1:
        promo = Piece('Hnight', c, C, 3, nwsq, img=fontpiecescol[1])
    else:
        promo = Piece('Queen', c, C, 9, nwsq, img=fontpiecescol[4])
    promo.moveimg()
    print 'Promotion: The new piece is a %s' % promo.type
    return promo

# function that moves pieces in the borddict
def movepiece(piece, oldsquare, newsquare):
    global borddict
    global fiftycount
    global Box
    global enpassantdict
    global situationsdict1
    global situationsdict2
    mycolor = piece.color
    oldpiece = borddict[newsquare]
    borddict[newsquare] = piece
    Piece('_ield', 'Neutr', 0, 0, oldsquare)
    if piece == kingslist[mycolor]:
        field_to_check = newsquare
    else:
        field_to_check = kingslist[mycolor].coord
    new_gen = attackgen(-mycolor, field_to_check)
    while 1:
        try:
            next(new_gen)
            borddict[newsquare] = oldpiece
            borddict[oldsquare] = piece
            return False
        except StopIteration:
            break
    del new_gen
    Box[oldpiece.color].append(oldpiece)
    if oldpiece.color != 0 or piece.type == 'Pawn':
        situationsdict1 = {}
        situationsdict2 = {}
        fiftycount = 0
    piece.unmoved = False
    piece.coord = newsquare
    piece.moveimg()
    borddict[oldsquare].moveimg()
    if newsquare in enpassantdict:
        passedpawn = enpassantdict[newsquare]
        del enpassantdict[newsquare]
        passedsquare = passedpawn.coord
        Piece('_ield', 'Neutr', 0, 0, passedsquare)
    print '%s from %r to %r' % (piece.name, oldsquare, newsquare)
    if piece.type == 'Pawn' and oldsquare[1] - newsquare[1] == -2:
        enpassantdict[(oldsquare[0], oldsquare[1]+1)] = piece
    if piece.type == 'Pawn' and newsquare[1] in [8, 1]:
        newpiece = picknewpiece(piece, newsquare)
        
    return True

# function that checks if a field is being attacked
def attackgen(attackingcolor, field_to_check):
        piecesonboard = givepieces(attackingcolor)
        for i in piecesonboard:
            piece, square = i
            moveslist = viable_steps(piece)
            if piece.type == 'Pawn':
                moveslist = [f for f in moveslist if f[0] != square[0]]
            if len(moveslist):
                for new in moveslist:
                    if new == field_to_check:
                        yield (piece, square)

# function that lists all pieces of a color in play
def givepieces(curcolor):
    piecesonboard = []
    for item in borddict.items():
        square, piece = item
        if piece.color == curcolor:
            piecesonboard.append((piece, square))
        else:
            continue
    return piecesonboard

# function that determines possibilities of castling
def castlecheck(color):
    castleoptions = []
    myking = kingslist[color]
    if not myking.unmoved:
        return castleoptions
    Rshort = rookslist[color][0]
    Rlong = rookslist[color][1]
    if not Rshort.unmoved and not Rlong.unmoved:
        return castleoptions
    castlingsquareslist = [
                                            ['dummy'],
                                            [
                                                [(6, 8), (7, 8)],
                                                [(2, 8), (3, 8), (4, 8)]
                                            ],
                                            [
                                                [(6, 1), (7, 1)],
                                                [(2, 1), (3, 1), (4, 1)]
                                            ]
                                          ]
    mycsquares = castlingsquareslist[color]
    bool_squarelist = [[], []]
    L = 0
    for squarelist in mycsquares:
        for square in squarelist:
            Agen = attackgen(-color, square)
            try:
                next(Agen)
                attack = True
            except StopIteration:
                attack = False
            if square[0] == 2:
                if not borddict[square].color:
                    bool_squarelist[L].append(True)
            else:
                if not attack and not borddict[square].color:
                    bool_squarelist[L].append(True)
            del Agen
        L += 1
    if Rshort.unmoved and len(bool_squarelist[0]) == 2:
        castleoptions.append([[myking, mycsquares[0][1]],
                                              [Rshort, mycsquares[0][0]]])
    if Rlong.unmoved and len(bool_squarelist[1]) == 3:
        castleoptions.append([[myking, mycsquares[1][1]],
                                              [Rlong, mycsquares[1][2]]])
    return castleoptions

# function that saves gamestate including castling and enpassant options
def savegamestate(castleopsboth):
    global situationsdict1
    global situationsdict2
    situationstring = ''
    for item in sorted(borddict.items(), key=lambda x: str(x[0]) + str(x[1])):
        field, piece = item
        situationstring += (str(piece.name) + str(field))
    for item in enpassantdict.items():
        situationstring += str(item)
    for item in castleopsboth:
        situationstring += str(item)
    hashedstring = hash(situationstring)
    if hashedstring in situationsdict1:
        print 'Same situation twice!'
        if hashedstring in situationsdict2:
            return True
        else:
            situationsdict2[hashedstring] = 1
            return
    else:
        situationsdict1[hashedstring] = 1
        return

# controller
def newgame(curcolor):
    global hascastled
    global enpassantdict
    global count
    global check
    global fiftycount
    while 1:
        if fiftycount == 50:
            return '50 without capturing a piece or pawn movement.'
        valid_move = False
        print
        print 'A new turn', count
        raw_input()
        hascastled = False
        curcolor = -curcolor
        castleops = castlecheck(curcolor)
        castleopsboth = castleops + castlecheck(-curcolor)
        if savegamestate(castleopsboth):
            return 'Three times the same situation! Draw.'
        if castleops and random.choice([0, 0, 0, 1]):
            moves = random.choice(castleops)
            for move in moves:
                movepiece(move[0], move[0].coord, move[1])
            valid_move = True
            hascastled = True
        piecesonboard = givepieces(curcolor)
        movesdict = {}
        for i in piecesonboard:
            piece, square = i
            moveslist = viable_steps(piece)
            if len(moveslist):
                movesdict[piece] = [[square, new] for new in moveslist]
        moveskeys = movesdict.keys()
        while not valid_move:
            if moveskeys:
                random.shuffle(moveskeys)
                chosenpiece = moveskeys.pop()
            else:
                if check:
                    return 'Checkmate!'
                else:
                    return 'Pat! Draw.'
            chosenoptions = movesdict[chosenpiece]
            random.shuffle(chosenoptions)
            while not valid_move:
                if not chosenoptions:
                    break
                mov = chosenoptions.pop()
                valid_move = movepiece(chosenpiece, mov[0], mov[1])
        new_checkgen = attackgen(curcolor, kingslist[-curcolor].coord)
        checkinglist = []
        done = False
        check = False
        while not done:
            try:
                checkinglist.append(next(new_checkgen))
                check = True
                for i in checkinglist:
                    print 'Checked by %s' % i[0].name
            except StopIteration:
                done = True
        count += 1
        fiftycount += 1
        del new_checkgen
        if len(enpassantdict):
            for piece in enpassantdict.values():
                if piece.color == -curcolor:
                    enpassantdict = {}
                    break




print newgame(1)
raw_input()
