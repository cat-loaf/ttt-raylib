#!/usr/bin/env python3

import sys
from pathlib import Path
from raylib import *  # type: ignore

from ttt_raylib import Glob, TicTacToe
from ttt_raylib.utils import aabb_rect, changeMouseCursor
from ttt_raylib.consts import GameState, PLAYING_STATES

glob = Glob()
drawg = Glob()
def on_resize(width, height):
    glob["screenWidth"] = width
    glob["screenHeight"] = height
    glob["midpointX"] = width / 2
    glob["midpointY"] = height / 2
    drawg["gap"] = int(min(width, height) / 20)
    drawg["size"] = int((min(width, height) - (drawg["gap"] * 4)) / 3)

def init():
    glob["screenWidth"] = 250
    glob["screenHeight"] = 250
    glob["midpointX"] = glob["screenWidth"] / 2
    glob["midpointY"] = glob["screenHeight"] / 2
    glob["targetFPS"] = 30
    
    glob["gameState"] = GameState.TURN_A
    glob["game"] = TicTacToe()

    drawg["gap"] = int(min(glob["screenWidth"], glob["screenHeight"]) / 20)
    drawg["size"] = int((min(glob["screenWidth"], glob["screenHeight"]) - (drawg["gap"] * 4)) / 3)
    drawg["round"] = 0
    drawg["thick"] = 2
    drawg["borderCol"] = DARKGRAY
    drawg["bgCol"] = LIGHTGRAY
    drawg["highlightCol"] = {
        GameState.TURN_A: [0, 255, 68, 64],
        GameState.TURN_B: [0, 157, 255, 64],
    }
    drawg["pressedCol"] = {
        GameState.TURN_A: [0, 255, 68, 128],
        GameState.TURN_B: [0, 157, 255, 128],
    }

    screen_init()
    
def screen_init():
    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_MSAA_4X_HINT)
    
    InitWindow(glob["screenWidth"], glob["screenHeight"], b"TicTacToe")
    SetWindowMinSize(250, 250)
    
    SetTargetFPS(glob["targetFPS"])
    
    
    icon = LoadImage(str(Path("./ttt-icon.png").resolve()).encode())
    print(str(Path("./ttt-icon.png").resolve()))
    SetWindowIcon(icon)

def update():
    while not WindowShouldClose():
        predraw()
        draw()
        postdraw()
    CloseWindow()
    
def predraw():
    glob["mousePos"] = GetMousePosition()
    
    if IsWindowResized():
        on_resize(GetScreenWidth(), GetScreenHeight())
        
    glob["mouseLeft"] = IsMouseButtonDown(MOUSE_BUTTON_LEFT)
    glob["mouseLeftPressed"] = IsMouseButtonPressed(MOUSE_BUTTON_LEFT)

def draw():
    BeginDrawing()
    ClearBackground(RAYWHITE)
    
    hovering_matrix = [[False for _ in range(3)] for _ in range(3)]
    
    for i in range(-1,2):
        for j in range(-1,2):
            rect: list[int] = [
                int(glob["midpointX"] + (j*drawg["size"]) + (j*drawg["gap"]) - (drawg["size"]/2)),
                int(glob["midpointY"] + (i*drawg["size"]) + (i*drawg["gap"]) - (drawg["size"]/2)),
                drawg["size"],
                drawg["size"]
            ]
            is_hovering = aabb_rect(
                rect,
                glob["mousePos"].x,
                glob["mousePos"].y
            )
            hovering_matrix[i+1][j+1] = is_hovering
            if is_hovering:
                changeMouseCursor(True)
                if glob["mouseLeft"] and glob["gameState"] in PLAYING_STATES:
                    col = drawg["pressedCol"].get(glob["gameState"], drawg["borderCol"])
                else:
                    col = drawg["highlightCol"].get(glob["gameState"], drawg["bgCol"])
                    
                DrawRectangleRounded(
                    rect,
                    drawg["round"],
                    10,
                    col
                )
            DrawRectangleRoundedLinesEx(
                rect, 
                drawg["round"], 
                10,
                drawg["thick"], 
                drawg["borderCol"]
            )
            
            is_pressed = is_hovering and glob["mouseLeftPressed"] and glob["gameState"] in PLAYING_STATES

            if is_pressed:
                res = glob["game"].makeMove(i+1, j+1)
                if res not in PLAYING_STATES:
                    glob["gameState"] = res
                else:
                    glob["gameState"] = glob["game"].current_player
            
            cell_state = glob["game"].get(j+1, i+1)
            DrawText(cell_state.encode(), int(rect[0] + drawg["gap"]/2), int(rect[1]+drawg["gap"]/2), drawg["size"], BLACK)
            
    if (glob["gameState"] in PLAYING_STATES):
        any_hovering = any(any(row) for row in hovering_matrix)
        changeMouseCursor(any_hovering)
    else:
        changeMouseCursor(False)
        win_text = {GameState.WIN_A: 'X won!',
                     GameState.WIN_B: 'O won!',
                     GameState.TIE: "Noone won :("}.get(glob["gameState"], "")
        txth = int(drawg["gap"]*2)
        backing_size = MeasureText(win_text.encode(), txth)
        DrawRectangle(0,0,backing_size+8,txth,drawg["pressedCol"].get(glob["game"].checkWinner(), [0xea,0xef,0xef,0xff]))
        DrawText(win_text.encode(), 4,0, txth, BLACK)

        text=b"Press 'R' to restart game"
        DrawRectangle(0,glob["screenHeight"]-txth,MeasureText(text, txth), txth, [0xea,0xef,0xef,0xff])
        DrawText(text, 2, glob["screenHeight"]-txth+4, txth, BLACK)

    EndDrawing()
    
def postdraw():
    if glob["gameState"] not in PLAYING_STATES:
        if IsKeyPressed(KEY_R):
            glob["game"] = TicTacToe()
            glob["gameState"] = GameState.TURN_A

def main():
    if "--debug" in sys.argv:
        SetTraceLogLevel(LOG_ALL)
    else:
        SetTraceLogLevel(LOG_NONE)
    
    init()
    update()
    
if __name__ == "__main__":
    main()