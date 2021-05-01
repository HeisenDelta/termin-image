#include <iostream>
#include <signal.h>
#include <termios.h>
#include <stdio.h>
#include <unistd.h>


typedef enum {
    KP_ECHO_OFF,
    KP_ECHO_ON,
} kp_echo_t;

int keypress(const kp_echo_t echo) {

    struct termios savedState;
    struct termios newState;
    unsigned char echo_bit;                                                 // enable/disable echo.  logic is reversed
    int c;

    if (-1 == tcgetattr(STDIN_FILENO, &savedState)) return EOF;             // error on tcgetattr

    newState = savedState;

    if (KP_ECHO_OFF == echo) echo_bit = ECHO;                               // echo bit set to disable echo
    else echo_bit = 0;                                                      // echo bit cleared to enable echo  

    // use canonical input and set echo.  set minimal input to 1.
    newState.c_lflag &= ~(echo_bit | ICANON);
    newState.c_cc[VMIN] = 1;

    if (-1 == tcsetattr(STDIN_FILENO, TCSANOW, &newState)) return EOF;      // error on tcsetattr

    c = getchar();                                                          // block (without spinning) until we get a key press

    // restore the saved state
    if (-1 == tcsetattr(STDIN_FILENO, TCSANOW, &savedState)) return EOF;    // error on tcsetattr

    return c;

}
