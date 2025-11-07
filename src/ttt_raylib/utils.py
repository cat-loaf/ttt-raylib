#!/usr/bin/env python3

from raylib import SetMouseCursor, MOUSE_CURSOR_DEFAULT, MOUSE_CURSOR_POINTING_HAND

def aabb(posX, posY, sizeX, sizeY, mouseX, mouseY) -> bool:
    return (posX <= mouseX <= posX + sizeX) and (posY <= mouseY <= posY + sizeY)

def aabb_rect(rect: list[int], mouseX: float, mouseY: float) -> bool:
    return aabb(rect[0], rect[1], rect[2], rect[3], mouseX, mouseY)

def changeMouseCursor(hover: bool):
    if hover:
        SetMouseCursor(MOUSE_CURSOR_POINTING_HAND)
    else:
        SetMouseCursor(MOUSE_CURSOR_DEFAULT)
        

