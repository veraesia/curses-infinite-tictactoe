
import curses
import time

import sprites

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

#persistent variables
caught_input = ""

height = curses.LINES
width = curses.COLS

board_win = curses.newwin(24, 40, 1, 8)
info_win = curses.newwin(12, 14, 1, 48)
value_matrix = [[0,0,0],[0,0,0],[0,0,0]]
cursor_matrix = [[],[],[]]
mark_matrix = [[],[],[]]

cursor_pos = [1,1]
count_flag = False
turn_swap = True
turn_count = 0
reset_flag = False
reset_wait = False
winner = 0

for i in range(0, 3):
	for j in range(0, 3):
		temp = curses.newwin(5, 10, (i*6)+3, (j*12)+10)
		cursor_matrix[i].append(temp)

for i in range(0, 3):
	for j in range(0, 3):
		temp = curses.newwin(5, 6, (i*6)+3, (j*12)+12)
		mark_matrix[i].append(temp)

while(True):

	#reset
	if (reset_flag):
		value_matrix = [[0,0,0],[0,0,0],[0,0,0]]
		cursor_pos = [1,1]
		count_flag = False
		turn_swap = True
		turn_count = 0
		reset_flag = False
		reset_wait = False
		winner = 0

	#screen update
	stdscr.clear()
	stdscr.addstr(0, 0, "TEST DISPLAY", curses.A_REVERSE)
	stdscr.addstr(height - 1, 0, ("Input: " + caught_input))
	stdscr.addstr(height - 1, width - 24, ("Height: " + str(height) + " Width: " + str(width)))
	stdscr.refresh()

	#info display
	info_win.clear()
	info_win.addstr(0, 0, sprites.info_board)
	if(turn_swap):
		info_win.addstr(2, 1, "X's Turn", curses.A_REVERSE)
	else:
		info_win.addstr(2, 1, "O's Turn", curses.A_REVERSE)
	if (winner == 1):
		info_win.addstr(4, 3, "X WINS!!!", curses.A_BOLD)
	elif (winner == -1):
		info_win.addstr(4, 3, "O WINS!!!", curses.A_BOLD)
	info_win.addstr(6, 1, ("Turn: " + str(turn_count)))
	info_win.addstr(7, 1, "(R) Restart")
	info_win.addstr(8, 1, "(Z) Place")
	info_win.refresh()

	#board background display
	board_win.clear()
	board_win.addstr(0, 0, sprites.board)
	board_win.refresh()

	#cursor display
	for i in range(0, 3):
		for j in range(0, 3):
			cursor_matrix[i][j].clear()
			cursor_matrix[i][j].refresh()

	cursor_matrix[cursor_pos[0]][cursor_pos[1]].addstr(0, 0, sprites.cursor)
	cursor_matrix[cursor_pos[0]][cursor_pos[1]].refresh()

	#value downstep
	if (count_flag):
		for i in range(0, 3):
			for j in range(0, 3):
				if ((value_matrix[i][j] < 0) and (turn_swap)):
					value_matrix[i][j] = value_matrix[i][j] + 1
				elif ((value_matrix[i][j] > 0) and not(turn_swap)):
					value_matrix[i][j] = value_matrix[i][j] - 1
		count_flag = False

	#value to sprite display
	for i in range(0, 3):
		for j in range(0, 3):
			mark_matrix[i][j].clear()

			match value_matrix[i][j]:
				case 1:
					mark_matrix[i][j].addstr(0, 0, sprites.cross2)
				case 2:
					mark_matrix[i][j].addstr(0, 0, sprites.cross1)
				case 3:
					mark_matrix[i][j].addstr(0, 0, sprites.cross)
				case -1:
					mark_matrix[i][j].addstr(0, 0, sprites.circle2)
				case -2:
					mark_matrix[i][j].addstr(0, 0, sprites.circle1)
				case -3:
					mark_matrix[i][j].addstr(0, 0, sprites.circle)
				case _:
					continue

			mark_matrix[i][j].refresh()

	#winner check
	#check all horizonal lines
	for i in range(0, 3):
		total = 0
		for j in range(0, 3):
			total = total + value_matrix[i][j]
		if (total == 6):
			winner = 1
			reset_wait = True
		elif (total == -6):
			winner = -1
			reset_wait = True

	#check all vertical lines
	for j in range(0, 3):
		total = 0
		for i in range(0, 3):
			total = total + value_matrix[i][j]
		if (total == 6):
			winner = 1
			reset_wait = True
		elif (total == -6):
			winner = -1
			reset_wait = True

	#check crosses
	total = value_matrix[0][0] + value_matrix[1][1] + value_matrix[2][2]
	if (total == 6):
		winner = 1
		reset_wait = True
	elif (total == -6):
		winner = -1
		reset_wait = True
	total = value_matrix[2][0] + value_matrix[1][1] + value_matrix[0][2]
	if (total == 6):
		winner = 1
		reset_wait = True
	elif (total == -6):
		winner = -1
		reset_wait = True

	#user input start
	usr_input = stdscr.getch()
	if (usr_input == ord('q')):
		break
	elif (usr_input == ord('r')):
		reset_flag = True
	elif (usr_input == 0x102): #down key
		if (cursor_pos[0] < 2):
			cursor_pos[0] = cursor_pos[0] + 1
	elif (usr_input == 0x103): #up key
		if (cursor_pos[0] > 0):
			cursor_pos[0] = cursor_pos[0] - 1
	elif (usr_input == 0x105): #right key
		if (cursor_pos[1] < 2):
			cursor_pos[1] = cursor_pos[1] + 1
	elif (usr_input == 0x104): #left key
		if (cursor_pos[1] > 0):
			cursor_pos[1] = cursor_pos[1] - 1

	elif ((usr_input == ord('z')) and not(reset_wait)):
		if (value_matrix[cursor_pos[0]][cursor_pos[1]] == 0):
			if (turn_swap):
				value_matrix[cursor_pos[0]][cursor_pos[1]] = 4
			else:
				value_matrix[cursor_pos[0]][cursor_pos[1]] = -4
				
			count_flag = True
			turn_swap = not(turn_swap)
			turn_count = turn_count + 1

	caught_input = str(hex(usr_input))
	#end of main loop

#end curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()