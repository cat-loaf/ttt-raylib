#!/usr/bin/env python3

from enum import Enum, auto

class GameState(Enum):
    MENU = auto()

    TURN_A = auto()
    TURN_B = auto()

    TIE = auto()
    WIN_A = auto()
    WIN_B = auto()
    
    
PLAYING_STATES = (
    GameState.TURN_A, 
    GameState.TURN_B, 
    False, 
    True
)